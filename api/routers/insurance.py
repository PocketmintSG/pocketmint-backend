from fastapi import APIRouter

from api.models.response_models.common import BaseJSONResponse
from api.types.requests_types import StatusEnum

router = APIRouter()


@router.post("/create_insurance")
async def create_insurance():
    return BaseJSONResponse(
        status=StatusEnum.SUCCESS,
        message="Insurance successfully created!",
        status_code=200,
    )


@router.post("/read_insurance")
async def read_insurance():
    return BaseJSONResponse(
        status=StatusEnum.SUCCESS, message="Insurance read!", status_code=200
    )


@router.post("/list_insurance")
async def list_insurance():
    return BaseJSONResponse(
        status=StatusEnum.SUCCESS, message="Insurance listed!", status_code=200
    )


@router.post("/update_insurance")
async def update_insurance():
    return BaseJSONResponse(
        status=StatusEnum.SUCCESS, message="Insurance updated!", status_code=200
    )


@router.post("/delete_insurance")
async def delete_insurance():
    return BaseJSONResponse(
        status=StatusEnum.SUCCESS, message="Insurance deleted!", status_code=200
    )
