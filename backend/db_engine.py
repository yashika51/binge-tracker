from sqlalchemy import create_engine
from models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./binge-tracker.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(bind=engine)
