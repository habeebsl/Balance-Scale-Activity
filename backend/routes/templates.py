from fastapi import APIRouter, Depends, status

import models
from schemas import ActivityResponse
from dependencies.auth_dependency import verify_token
from dependencies.db_dependency import db_dependency

template_router = APIRouter()

@template_router.get("/templates", status_code=status.HTTP_200_OK, response_model=list[ActivityResponse])
async def get_templates(db: db_dependency, token=Depends(verify_token)):
    uid = token["uid"]
    user = db.query(models.User).filter(models.User.uid == uid).first()
    user_templates = db.query(models.Activity).filter(models.Activity.user == user)
    
    return user_templates.all()