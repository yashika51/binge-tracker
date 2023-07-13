from fastapi import APIRouter, Depends
from database_operations import DatabaseOperations
from schemas import ShowRequest, ShowResponse

router = APIRouter()


@router.get("/users/{user_id}/shows")
def get_all_shows(
    user_id: int, db_operations: DatabaseOperations = Depends(DatabaseOperations)
):
    return db_operations.get_all_shows(user_id)


@router.post("/users/{user_id}/shows")
def add_show(
    user_id: int,
    show: ShowRequest,
    db_operations: DatabaseOperations = Depends(DatabaseOperations),
):
    return db_operations.add_show(user_id, show)


@router.delete("/users/{user_id}/shows/{show_id}")
def delete_show(
    user_id: int,
    show_id: int,
    db_operations: DatabaseOperations = Depends(DatabaseOperations),
):
    return db_operations.delete_show(user_id, show_id)
