import pytest
from fastapi.testclient import TestClient
from dependencies.auth_dependency import verify_token
from dependencies.db_dependency import get_db
from main import app
from database import Base
from tests.dependencies.mock_auth_dependency import mock_verify_token
from tests.dependencies.mock_database import override_get_db, test_engine

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(autouse=True)
def db_fixture():
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[verify_token] = mock_verify_token
    yield
    app.dependency_overrides.clear()


def test_create_user():
    username = "testuser"
    expected_keys = ["uid", "email", "username", "role"]
    response = client.post(
        "/users/create",
        headers={"Authorization": "Bearer valid_token"},
        json={"username": username}
    )
    response_json = response.json()
    assert response.status_code == 201
    assert set(response_json.keys()) == set(expected_keys)


def test_create_same_user_again():
    first_response = client.post(
        "/users/create",
        headers={"Authorization": "Bearer valid_token"},
        json={"username": "testuser"}
    )
    assert first_response.status_code == 201
    second_response = client.post(
        "/users/create",
        headers={"Authorization": "Bearer valid_token"},
        json={"username": "testuser"}
    )
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "User with this email already exists."


def test_create_user_invalid_token():
    app.dependency_overrides[verify_token] = mock_verify_token
    username = "testuser"
    response = client.post(
        "/users/create",
        headers={"Authorization": "Bearer invalid_token"},
        json={"username": username}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid Auth token"
