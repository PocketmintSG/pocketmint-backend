from bson import ObjectId
from fastapi import APIRouter, Depends
from pymongo import MongoClient

from api.models.response_models.common import (
    BaseHTTPException,
    BaseJSONResponse,
    BaseResponseModel,
)
from api.models.response_models.insurance import InsuranceModel
from api.types.requests_types import StatusEnum
from api.utils.database import get_cluster_connection
from api.utils.requests_utils import dict_to_json, model_to_dict
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


@router.get(
    "/get_insurance/{insurance_id}",
    response_model=BaseResponseModel[InsuranceModel],
    dependencies=[Depends(verify_token)],
)
async def read_insurance(
    insurance_id: str, cluster: MongoClient = Depends(get_cluster_connection)
):
    insurance_db = cluster["pocketmint"]["insurance_details"]
    res = insurance_db.find_one({"_id": ObjectId(insurance_id)})
    print(res)
    if not res:
        raise BaseHTTPException(
            status=StatusEnum.FAILURE,
            status_code=404,
            message="Insurance not found!",
        )

    return BaseJSONResponse(
        status=StatusEnum.SUCCESS,
        message="Insurance found!",
        status_code=200,
        data=dict_to_json(res),
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
