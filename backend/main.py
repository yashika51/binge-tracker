from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from db_connection import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

# app.include_router()