import json
import pyrebase
import os

from firebase_admin import credentials
from fastapi import APIRouter
from api.models.response_models.common import BaseJSONResponse
from api.types.requests_types import StatusEnum
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

with open("firebase_config.json") as config_file:
    config = json.load(config_file)


pb = pyrebase.initialize_app(config)
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")


@router.get("/get_token")
async def get_token():
    user = pb.auth().sign_in_with_email_and_password(ADMIN_EMAIL, ADMIN_PASSWORD)
    return BaseJSONResponse(
        status=StatusEnum.SUCCESS,
        message="Token retrieved!",
        status_code=200,
        data={"token": "Bearer " + user["idToken"]},
    )
