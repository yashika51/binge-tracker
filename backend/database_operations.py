from fastapi import HTTPException, status
from fastapi import Depends
from sqlalchemy import asc
from sqlalchemy.orm import Session
import logging
from typing import Optional, List, Tuple
from db_engine import engine, get_db
from models import User, Show, Episode
from sqlalchemy.exc import IntegrityError
from schemas import UserRequest, UserResponse, ShowRequest, ShowResponse
from schemas import EpisodeRequest, EpisodeResponse
from utils import get_password_hash, verify_password


class DatabaseOperations:
    def __init__(self, db: Session = Depends(get_db)):
        self._engine = engine
        self._logger = logging.getLogger(self.__class__.__name__)
        self.db = db

    def authenticate_user(self, username: str, password: str):
        user_email, hashed_password = self.get_user_data(username)
        if not user_email:
            return False
        if not verify_password(password, hashed_password):
            return False
        return user_email

    def get_user_data(self, email: str) -> Optional[Tuple[str, str]]:
        user = self.db.query(User).filter(User.email == email).first()
        if user:
            return user.email, user.password
        return None

    def create_user(self, user: UserRequest) -> UserResponse:
        hashed_password = get_password_hash(user.password)
        db_user = User(name=user.name, email=user.email, password=hashed_password)
        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists.",
            )
        return UserResponse(
            id=db_user.id, name=db_user.name, email=db_user.email, shows=[]
        )

    def get_all_shows(self, user_id: int) -> List[ShowResponse]:
        shows = self.db.query(Show).filter(Show.user_id == user_id).all()
        return [ShowResponse(**show.__dict__) for show in shows]

    def add_show(self, user_id: int, show: ShowRequest) -> ShowResponse:
        show.title = show.title.lower()
        existing_show = (
            self.db.query(Show)
            .filter(Show.title == show.title, Show.user_id == user_id)
            .first()
        )
        if existing_show:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Show with this title already exists for the user.",
            )

        new_show = Show(**show.model_dump(), user_id=user_id)
        self.db.add(new_show)
        self.db.commit()
        self.db.refresh(new_show)
        return ShowResponse(**new_show.__dict__)

    def delete_show(self, user_id: int, show_id: int) -> Optional[ShowResponse]:
        show = (
            self.db.query(Show)
            .filter(Show.user_id == user_id, Show.id == show_id)
            .first()
        )
        if show:
            show_data = ShowResponse(**show.__dict__)
            self.db.delete(show)
            self.db.commit()
            return show_data
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Show does not exists for the user.",
        )

    def get_show_episodes(self, user_id: int, show_id: int) -> List[EpisodeResponse]:
        episodes = (
            self.db.query(Episode)
            .join(Show)
            .filter(Show.id == show_id, Show.user_id == user_id)
            .all()
        )
        return [
            EpisodeResponse(
                id=episode.id,
                title=episode.title,
                watched=episode.watched,
                show_id=episode.show_id,
            )
            for episode in episodes
        ]

    def add_episode(
        self, user_id: int, show_id: int, episode: EpisodeRequest
    ) -> Optional[EpisodeResponse]:
        show = (
            self.db.query(Show)
            .filter(Show.id == show_id, Show.user_id == user_id)
            .first()
        )
        if not show:
            return None

        new_episode = Episode(
            title=episode.title, watched=episode.watched, show_id=show_id
        )
        self.db.add(new_episode)
        self.db.commit()
        self.db.refresh(new_episode)
        return EpisodeResponse(
            id=new_episode.id,
            title=new_episode.title,
            watched=new_episode.watched,
            show_id=new_episode.show_id,
        )

    def delete_episode(self, user_id: int, show_id: int, episode_id: int):
        episode = (
            self.db.query(Episode)
            .join(Show)
            .filter(
                Show.id == show_id, Show.user_id == user_id, Episode.id == episode_id
            )
            .first()
        )
        if episode:
            self.db.delete(episode)
            self.db.commit()
        return episode

    def mark_episode_as_watched(
        self, user_id: int, show_id: int, episode_id: int
    ) -> Optional[EpisodeResponse]:
        episode = (
            self.db.query(Episode)
            .join(Show)
            .filter(
                Show.id == show_id, Show.user_id == user_id, Episode.id == episode_id
            )
            .first()
        )
        if episode:
            episode.watched = True
            self.db.commit()
            return EpisodeResponse(
                id=episode.id,
                title=episode.title,
                watched=episode.watched,
                show_id=episode.show_id,
            )
        return None

    def get_next_episode(self, user_id: int, show_id: int) -> Optional[EpisodeResponse]:
        db_episode = (
            self.db.query(Episode)
            .join(Show)
            .filter(
                Episode.show_id == show_id,
                Show.viewer_id == user_id,
                Episode.watched == False,
            )
            .order_by(asc(Episode.id))
            .first()
        )
        if db_episode:
            return EpisodeResponse(**db_episode.__dict__)
        return None

    def get_show_list_with_next_episode(self, user_id: int) -> List[ShowResponse]:
        db_shows = self.db.query(Show).filter(Show.viewer_id == user_id).all()

        show_list = []
        for db_show in db_shows:
            next_episode = self.get_next_episode(user_id, db_show.id)
            show = ShowResponse(
                id=db_show.id,
                title=db_show.title,
                episodes=[
                    EpisodeResponse(**episode.__dict__) for episode in db_show.episodes
                ],
                watched_episodes=[
                    EpisodeResponse(**episode.__dict__)
                    for episode in db_show.episodes
                    if episode.watched
                ],
                next_episode=next_episode,
            )
            show_list.append(show)

        return show_list
