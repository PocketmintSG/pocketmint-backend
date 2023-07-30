from fastapi import APIRouter, Depends
from pymongo import MongoClient

from api.models.response_models.common import BaseJSONResponse, BaseResponseModel
from api.models.response_models.insurance import InsuranceModel
from api.types.requests_types import StatusEnum
from api.utils.database import get_cluster_connection
from api.utils.requests_utils import model_to_dict
from api.utils.security import verify_token

router = APIRouter()


@router.post(
    "/create_insurance",
    response_model=BaseResponseModel[InsuranceModel],
    dependencies=[Depends(verify_token)],
)
async def create_insurance(
    insurance_details: InsuranceModel,
    cluster: MongoClient = Depends(get_cluster_connection),
):
    insurance_db = cluster["pocketmint"]["insurance_details"]
    insurance_details = model_to_dict(insurance_details)
    res = insurance_db.insert_one(insurance_details)

    insurance_details["_id"] = str(res.inserted_id)

    return BaseJSONResponse(
        status=StatusEnum.SUCCESS,
        message="Insurance successfully created!",
        status_code=200,
        data=insurance_details,
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
