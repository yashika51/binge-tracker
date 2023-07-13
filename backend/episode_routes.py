from fastapi import APIRouter, Depends
from database_operations import DatabaseOperations
from typing import List
from schemas import EpisodeRequest, EpisodeResponse

router = APIRouter()


@router.get(
    "/users/{user_id}/shows/{show_id}/episodes", response_model=List[EpisodeResponse]
)
def get_show_episodes(
    user_id: int,
    show_id: int,
    db_operations: DatabaseOperations = Depends(DatabaseOperations),
):
    return db_operations.get_show_episodes(user_id, show_id)


@router.post(
    "/users/{user_id}/shows/{show_id}/episodes", response_model=EpisodeResponse
)
def add_episode(
    user_id: int,
    show_id: int,
    episode: EpisodeRequest,
    db_operations: DatabaseOperations = Depends(DatabaseOperations),
):
    return db_operations.add_episode(user_id, show_id, episode)


@router.delete("/users/{user_id}/shows/{show_id}/episodes/{episode_id}")
def delete_episode(
    user_id: int,
    show_id: int,
    episode_id: int,
    db_operations: DatabaseOperations = Depends(DatabaseOperations),
):
    return db_operations.delete_episode(user_id, show_id, episode_id)


@router.put(
    "/users/{user_id}/shows/{show_id}/episodes/{episode_id}/watched",
    response_model=EpisodeResponse,
)
def mark_episode_as_watched(
    user_id: int,
    show_id: int,
    episode_id: int,
    db_operations: DatabaseOperations = Depends(DatabaseOperations),
):
    return db_operations.mark_episode_as_watched(user_id, show_id, episode_id)
