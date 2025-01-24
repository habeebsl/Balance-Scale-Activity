from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from firebase_admin import auth

import models
from dependencies.db_dependency import db_dependency
from dependencies.auth_dependency import verify_token
from schemas import UserBase, UserResponse, RoleRequest


user_router = APIRouter()

@user_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(db: db_dependency, request_data: Optional[UserBase] = None, token=Depends(verify_token)):
    uid = token["uid"]
    
    existing_user = db.query(models.User).filter(models.User.email == token["email"]).first()
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="User with this email already exists."
        )
    
    username = request_data.username if request_data and request_data.username else token['name'].replace(" ", "_")
    print(uid)

    db_user = models.User(
        uid=uid,
        username=username,
        email=token['email']
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@user_router.post("/set-user-role", status_code=status.HTTP_201_CREATED)
async def set_user_role(request_data: RoleRequest, db: db_dependency, token=Depends(verify_token)):
    try:
        uid = token['uid']
        auth.set_custom_user_claims(uid, {'role': request_data.role})
        user = db.query(models.User).filter(models.User.uid == uid).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found in database"
            )

        user.role = request_data.role
        db.commit()
        db.refresh(user)

        return {"success": True}
    except Exception as e:
        print("error: ", str(e))
        return {"error": str(e)}
