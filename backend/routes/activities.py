from typing import Optional
from fastapi import APIRouter, status, Depends, HTTPException, Query
from sqlalchemy.orm import joinedload

import models
from schemas import ActivityResponse, CreateActivity, UpdateActivity, PublishedActivityResponse, GetActivityResponseModel
from dependencies.db_dependency import db_dependency
from dependencies.auth_dependency import verify_token


activity_router = APIRouter()

@activity_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=ActivityResponse)
async def create_activity(request_data: CreateActivity, db: db_dependency, token=Depends(verify_token)):
    try:
        print("before")
        uid = token["uid"]
        user = db.query(models.User).filter(models.User.uid == uid).first()
        db_activity = models.Activity(
            name=request_data.name,
            published=request_data.published,
            difficulty=request_data.difficulty,
            user=user
        )

        db.add(db_activity)
        print("Added activity")

        for problem in request_data.problemset:
            db_problem = models.Problem(
                activity=db_activity,
                **problem.model_dump()
            )
            db.add(db_problem)

        db.commit()
        db.refresh(db_activity)

        print(db_activity)
        return db_activity
    except Exception as e:
        print(str(e))


@activity_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=GetActivityResponseModel)
async def get_activity(id: str, db: db_dependency, token=Depends(verify_token)):
    uid = token["uid"]

    activity = db.query(models.Activity).filter(models.Activity.id == id).first()

    if not activity:
        raise HTTPException(status_code=404, detail="Activity Not Found")

    is_creator = activity.user_id == uid
    print("user_id: ", activity.user_id)

    if not activity.published and not is_creator:
        raise HTTPException(status_code=403, detail="You are not allowed to access this activity")

    response = {
        "activity": activity, 
        "can_edit": is_creator
    }

    return response

@activity_router.put("/{id}", status_code=status.HTTP_200_OK, response_model=ActivityResponse)
async def update_activity(id: str, request: UpdateActivity, db: db_dependency, token=Depends(verify_token)):
    activity = db.query(models.Activity).filter(models.Activity.id == id).first()
    
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
    
    update_data = request.model_dump(exclude_unset=True)
    problemset_data = update_data.pop("problemset", None)
    
    if update_data:
        db.query(models.Activity).filter(models.Activity.id == id).update(update_data)

    if problemset_data:
        print(True)
        for problem in problemset_data:
            print(True)
            problem_id = problem.pop("id", None)
            if not problem_id:
                db_problem = models.Problem(
                    activity=activity,
                    **problem
                )
                db.add(db_problem)
            else:
                db.query(models.Problem).filter(models.Problem.id == problem_id).update(problem)

    db.commit()
    db.refresh(activity)

    return activity


@activity_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity(id: str, db: db_dependency, token=Depends(verify_token)):
    activity = db.query(models.Activity).filter(models.Activity.id == id).first()

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Activity with ID {id} not found."
        )
    
    db.delete(activity)
    db.commit()
    return


@activity_router.get("", status_code=status.HTTP_200_OK, response_model=list[PublishedActivityResponse])
async def list_activities(db: db_dependency, activity_limit: Optional[int] = Query(None, ge=1), token=Depends(verify_token)):
    print("Started something")
    activities = db.query(models.Activity)\
                .options(joinedload(models.Activity.user))\
                .filter(models.Activity.published == True)


    if activity_limit:
        activities = activities.limit(activity_limit)
    
    result = []
    for activity in activities.all():
        activity_dict = {
            'id': activity.id,
            'name': activity.name,
            'difficulty': activity.difficulty,
            'published': activity.published,
            'last_modified': activity.last_modified,
            'problemset': activity.problemset,
            'username': activity.user.username if activity.user else None
        }

        result.append(activity_dict)
    
    return result
