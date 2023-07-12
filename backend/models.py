from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

class Show(Base):
    __tablename__ = "shows"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="shows")

class Episode(Base):
    __tablename__ = "episodes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    watched = Column(Boolean, default=False)
    show_id = Column(Integer, ForeignKey("shows.id"))

    show = relationship("Show", back_populates="episodes")

# Relationships
User.shows = relationship("Show", back_populates="user", cascade="all, delete, delete-orphan")
Show.episodes = relationship("Episode", back_populates="show", cascade="all, delete, delete-orphan")
