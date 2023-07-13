from fastapi import APIRouter, Depends, HTTPException, status
from database_operations import DatabaseOperations
from schemas import EpisodeRequest, EpisodeResponse

router = APIRouter()


@router.put("/users/{user_id}/shows/{show_id}/episodes/{episode_id}", response_model=EpisodeResponse)
def mark_episode_as_watched(user_id: int, show_id: int, episode_id: int, db_operations: DatabaseOperations = Depends(DatabaseOperations)):
    return db_operations.mark_episode_as_watched(user_id, show_id, episode_id)
