import os

from fastapi import APIRouter
from api.routers import auth, utils, insurance, internal
from dotenv import load_dotenv

load_dotenv()

api_router = APIRouter()
api_router.include_router(auth.router, tags=["Authentication"])
api_router.include_router(utils.router, tags=["Utils"])
api_router.include_router(insurance.router, tags=["Insurance"])

# Only include internal routes if the environment is development
if os.environ.get("ENV") == "dev":
    api_router.include_router(internal.router, tags=["Internal"])
