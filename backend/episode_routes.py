from fastapi import APIRouter, Depends, HTTPException, status
from database_operations import DatabaseOperations
from typing import List
from schemas import EpisodeRequest, EpisodeResponse, ShowResponse

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


@router.get(
    "/users/{user_id}/shows/{show_id}/next_episode", response_model=EpisodeResponse
)
def get_next_episode(
    user_id: int,
    show_id: int,
    db_operations: DatabaseOperations = Depends(DatabaseOperations),
):
    next_episode = db_operations.get_next_episode(user_id, show_id)
    if not next_episode:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No next episode found for the show.",
        )
    return next_episode


@router.get(
    "/users/{user_id}/shows-with-next-episode", response_model=List[ShowResponse]
)
def get_show_list_with_next_episode(
    user_id: int, db_operations: DatabaseOperations = Depends(DatabaseOperations)
):
    shows = db_operations.get_all_shows(user_id)
    for show in shows:
        next_episode = db_operations.get_next_episode(user_id, show.id)
        show.next_episode = next_episode
    return shows
