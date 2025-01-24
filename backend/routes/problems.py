from fastapi import APIRouter, HTTPException, status, Depends
from schemas import DeleteProblems

import models
from dependencies.db_dependency import db_dependency
from dependencies.auth_dependency import verify_token


problem_router = APIRouter()

@problem_router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)    
async def delete_problems(request_data: list[DeleteProblems], db: db_dependency, token=Depends(verify_token)):
    if not request_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No problems provided")
    
    for problem_data in request_data:
        problem = db.query(models.Problem).filter(models.Problem.id == problem_data.id).first()
        
        if not problem:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Problem with ID {problem_data.id} not found."
            )

        db.delete(problem)
        print(f"Deleted problem with ID: {problem_data.id}")

    db.commit()
    return
