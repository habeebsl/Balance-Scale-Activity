import pytest
from fastapi.testclient import TestClient
from main import app
from database import Base
from dependencies.auth_dependency import verify_token
from dependencies.db_dependency import get_db
from tests.dependencies.mock_uid import uid_manager
from tests.dependencies.mock_email import email_manager
from tests.dependencies.mock_auth_dependency import mock_verify_token
from tests.dependencies.mock_database import override_get_db, test_engine


client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def db_fixture():
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[verify_token] = mock_verify_token
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(db_fixture):
    response = client.post(
        "/api/users/create",
        headers={"Authorization": "Bearer valid_token"},
        json={"username": "testuser"}
    )
    user_data = response.json()
    uid_manager.save_uid(user_data["uid"])
    return user_data

@pytest.fixture
def test_activity(test_user):
    response = client.post(
        "/api/activities/create",
        headers={"Authorization": "Bearer valid_token"},
        json={
            "name": "Test Activity",
            "difficulty": "medium",
            "published": False,
            "problemset": [
                {
                "step": 1,
                "target": 100,
                "limit": 5,
                "difficulty": "medium"
                }
            ]
        }
    )
    return response

def test_create_activity(test_activity):
    data = test_activity.json()
    assert test_activity.status_code == 201
    assert data.get("id") is not None
    assert data["name"] == "Test Activity"

def test_get_activity(test_activity):
    activity_data = test_activity.json()
    response = client.get(
        f"/api/activities/{activity_data.get('id')}",
        headers={"Authorization": "Bearer valid_token"}
    )

    data = response.json()
    assert response.status_code == 200
    assert data.get("can_edit") == True

def test_activity_restriction(test_activity):
    uid_manager.reset_uid()
    email_manager.save_email("testuser2@gmail.com")
    response = client.post(
        "/api/users/create",
        headers={"Authorization": "Bearer valid_token"},
        json={"username": "testuser2"}
    )
    user_data = response.json()
    uid_manager.save_uid(user_data["uid"])
    activity_data = test_activity.json()

    response = client.get(
        f"/api/activities/{activity_data.get('id')}",
        headers={"Authorization": "Bearer valid_token"}
    )

    data = response.json()
    assert response.status_code == 403
    assert data["detail"] == "You are not allowed to access this activity"

def test_edit_activity(test_activity):
    activity_data = test_activity.json()
    json_input = activity_data.copy()
    json_input.pop("created_at")
    json_input.pop("id")
    json_input["name"] = "Template 2"
    json_input["problemset"][0]["target"] = 200
    response = client.put(
        f"/api/activities/{activity_data.get('id')}",
        headers={"Authorization": "Bearer valid_token"},
        json=json_input
    )

    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "Template 2"
    assert data["problemset"][0]["target"] == 200


def test_delete_activity(test_activity):
    activity_data = test_activity.json()
    response = client.delete(
        f"/api/activities/{activity_data.get('id')}",
        headers={"Authorization": "Bearer valid_token"}
    )

    assert response.status_code == 204