from fastapi import HTTPException, Header
import uuid
from tests.dependencies.mock_uid import uid_manager
from tests.dependencies.mock_email import email_manager


def mock_verify_token(authorization: str = Header(...)):
    if authorization == "Bearer valid_token":
        token = authorization.split("Bearer ")[1]
        test_user_uid = uid_manager.get_uid()
        test_user_email = email_manager.get_email()
        if token == "valid_token":
            return {
                "uid": f"{uuid.uuid4() if not test_user_uid else test_user_uid}",
                "email": "testuser@gmail.com" if not test_user_email else test_user_email
            }
        else:
           raise HTTPException(status_code=401, detail="Invalid Auth token") 
    else:
        raise HTTPException(status_code=401, detail="Invalid Auth token")