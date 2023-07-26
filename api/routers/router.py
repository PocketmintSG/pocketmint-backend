from fastapi import APIRouter
from api.routers import auth, utils

api_router = APIRouter()
api_router.include_router(auth.router, tags=["Authentication"])
api_router.include_router(utils.router, tags=["Utils"])
