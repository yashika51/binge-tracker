from fastapi import FastAPI
from fastapi import Depends
from database_operations import get_db
import user_routes, show_routes, episode_routes

app = FastAPI()

app.include_router(user_routes.router, prefix="/v1/users", tags=["users"], dependencies=[Depends(get_db)])
app.include_router(show_routes.router, prefix="/v1/shows", tags=["shows"], dependencies=[Depends(get_db)])
app.include_router(episode_routes.router, prefix="/v1/episodes", tags=["episodes"], dependencies=[Depends(get_db)])
