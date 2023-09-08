import json
import pyrebase
import os

from firebase_admin import credentials
from fastapi import APIRouter
from api.models.response_models.common import BaseHTTPException, BaseJSONResponse
from api.types.requests_types import StatusEnum
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# with open("firebase_config.json") as config_file:
#     config = json.load(config_file)


pb = pyrebase.initialize_app(
    {
        "apiKey": "AIzaSyC-MYIPxArSkkzyS0Gig-5JqX0iM4WC7mg",
        "authDomain": "pocketmint-frontend.firebaseapp.com",
        "projectId": "pocketmint-frontend",
        "storageBucket": "pocketmint-frontend.appspot.com",
        "messagingSenderId": "106285860508",
        "appId": "1:106285860508:web:05281520dc7d89150c4f59",
        "measurementId": "G-SDTG6MF8V9",
        "databaseURL": "https://pocketmint-frontend-default-rtdb.asia-southeast1.firebasedatabase.app/",
    }
)
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


@router.get("/test_response")
async def test_response():
    raise BaseHTTPException(
        status=StatusEnum.SUCCESS,
        message="Test response",
        status_code=400,
        data={"Test Key": "Test Value"},
    )
