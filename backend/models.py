from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    shows = relationship("Show", back_populates="viewer")


class Show(Base):
    __tablename__ = "shows"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    viewer = relationship("User", back_populates="shows")
    episodes = relationship("Episode", back_populates="parent_show")


class Episode(Base):
    __tablename__ = "episodes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    watched = Column(Boolean, default=False)
    show_id = Column(Integer, ForeignKey("shows.id"))
    parent_show = relationship("Show", back_populates="episodes")
