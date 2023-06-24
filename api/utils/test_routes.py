from fastapi import APIRouter, Request

utils_router = APIRouter()


@utils_router.get("/ping")
async def pong(request: Request):
    return {"message": "pong"}
