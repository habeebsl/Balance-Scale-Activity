from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    username: Optional[str] = None

class UserResponse(UserBase):
    uid: str
    role: Optional[str] = None
    username: Optional[str] = None
    email: EmailStr

class RoleRequest(BaseModel):
    role: str


# Problem Schemas
class Problem(BaseModel):
    step: int
    target: int
    limit: int
    difficulty: str
    time_limit: Optional[int] = None
    hint: Optional[str] = None

class UpdateProblem(Problem):
    id: Optional[str] = None

class DeleteProblems(BaseModel):
    id: str


# Activity Schemas
class ActivityBase(BaseModel):
    name: str
    difficulty: str
    published: bool
    
class CreateActivity(ActivityBase):
    problemset: list[Problem]

class UpdateActivity(ActivityBase):
    problemset: list[UpdateProblem]

    model_config = {
        "extra": "forbid"
    }
    
class ActivityResponse(ActivityBase):
    id: str
    created_at: datetime
    problemset: Optional[list[UpdateProblem]] = []

class GetActivityResponseModel(BaseModel):
    activity: ActivityResponse
    can_edit: bool

class PublishedActivityResponse(ActivityBase):
    id: str
    last_modified: datetime
    problemset: Optional[list[UpdateProblem]] = []
    username: str