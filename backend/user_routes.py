from fastapi import APIRouter, Depends
from database_operations import DatabaseOperations
from schemas import UserRequest, UserResponse

router = APIRouter()


@router.post("/users/", response_model=UserResponse)
def create_user(user: UserRequest, db_operations: DatabaseOperations = Depends(DatabaseOperations)):
    new_user = db_operations.create_user(user)
    return new_user

