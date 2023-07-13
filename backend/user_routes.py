from fastapi import APIRouter, Depends, HTTPException, status
from database_operations import DatabaseOperations
from fastapi.security import OAuth2PasswordRequestForm
from schemas import UserRequest, UserResponse

router = APIRouter()


@router.post("/users", response_model=UserResponse)
def create_user(user: UserRequest, db_operations: DatabaseOperations = Depends(DatabaseOperations)):
    new_user = db_operations.create_user(user)
    return new_user
@router.post("/users/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db_operations: DatabaseOperations = Depends(DatabaseOperations)):
    user = db_operations.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "Logged in successfully!"}