from fastapi import FastAPI, APIRouter
import user_routes
import show_routes

api_router = APIRouter(prefix="/v1")
api_router.include_router(user_routes.router)
api_router.include_router(show_routes.router)


app = FastAPI()
