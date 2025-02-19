from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine

from routes.activities import activity_router
from routes.problems import problem_router
from routes.templates import template_router
from routes.users import user_router


tags_metadata = [
    {
        "name": "users",
        "description": "Endpoints for managing users, such as creating users and adding user roles",
    },
    {
        "name": "activities",
        "description": "Endpoints for managing activities, including creating, updating, deleting and listing activities.",
    },
    {
        "name": "problems",
        "description": "Handles deleting problems from activities",
    },
    {
        "name": "templates",
        "description": "Template endpoint for retrieving user templates",
    },
]

app = FastAPI(openapi_tags=tags_metadata)
models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:4173", "https://balance-scale-activity.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Type", "Authorization"],
)

app.include_router(user_router, prefix="/api/users", tags=["users"])
app.include_router(activity_router, prefix="/api/activities", tags=["activities"])
app.include_router(problem_router, prefix="/api/problems", tags=["problems"])
app.include_router(template_router, prefix="/api", tags=["templates"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)