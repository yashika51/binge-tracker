import sqlalchemy as sa
from fastapi import HTTPException, status
from sqlalchemy import insert
from fastapi import Depends
from sqlalchemy.orm import Session
import logging
from typing import List
from db_engine import engine, get_db
from models import User, Show, Episode
from sqlalchemy.exc import IntegrityError
from schemas import UserBase, UserRequest, UserResponse, ShowResponse, ShowRequest
from utils import get_password_hash

class DatabaseOperations:
    def __init__(self, db: Session = Depends(get_db)):
        self._engine = engine
        self._logger = logging.getLogger(self.__class__.__name__)
        self.db = db

    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, user: UserRequest) -> UserResponse:
        hashed_password = get_password_hash(user.password)
        db_user = User(**user.model_dump(), hashed_password=hashed_password)
        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists."
            )
        return UserResponse(**db_user.dict())

    def get_all_shows(self, user_id: int):
        return self.db.query(Show).filter(Show.viewer_id == user_id).all()

    def add_show(self, user_id: int, show: ShowRequest):
        new_show = Show(**show.model_dump(), viewer_id=user_id)
        self.db.add(new_show)
        self.db.commit()
        return new_show

    def delete_show(self, user_id: int, show_id: int):
        show = self.db.query(Show).filter(Show.viewer_id == user_id, Show.id == show_id).first()
        if show:
            self.db.delete(show)
            self.db.commit()
        return show

