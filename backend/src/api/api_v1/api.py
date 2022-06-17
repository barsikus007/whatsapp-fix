from fastapi import APIRouter

from src.api.api_v1.endpoints import login, user, link


api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(link.router, prefix="/links", tags=["links"])
