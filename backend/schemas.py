from typing import List, Optional
from pydantic import BaseModel


class EpisodeBase(BaseModel):
    title: str
    watched: bool
    show_id: int


class EpisodeRequest(EpisodeBase):
    pass


class EpisodeResponse(EpisodeBase):
    id: int

    class Config:
        orm_mode = True


class ShowBase(BaseModel):
    title: str


class ShowRequest(ShowBase):
    pass


class ShowResponse(ShowBase):
    id: int
    episodes: List[EpisodeResponse] = []
    watched_episodes: List[EpisodeResponse] = []
    next_episode: Optional[EpisodeResponse] = None

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: str


class UserRequest(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    shows: List[ShowResponse] = []

    class Config:
        orm_mode = True
