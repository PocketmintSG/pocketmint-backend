from fastapi import APIRouter
from api.routers import auth

api_router = APIRouter()
api_router.include_router(auth.router, tags=["Authentication"])
