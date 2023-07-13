from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi import Depends
from database_operations import get_db
import user_routes, show_routes, episode_routes


app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes.router, tags=["users"], dependencies=[Depends(get_db)])
app.include_router(show_routes.router, tags=["shows"], dependencies=[Depends(get_db)])
app.include_router(episode_routes.router, tags=["episodes"], dependencies=[Depends(get_db)])
