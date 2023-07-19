import json
import pyrebase

from datetime import datetime
from fastapi.params import Depends
from firebase_admin import auth
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from pymongo import MongoClient
import requests
from api.configs.constants.exceptions import (
    GENERIC_EXCEPTION_MESSAGE,
)
from api.models.request_models.auth import (
    AuthRequest,
    ProfileChangePasswordRequest,
)
from api.models.response_models.common import (
    BaseHTTPException,
    BaseResponseModel,
    GeneralResponse,
)
from api.models.user import User
from api.types.requests_types import StatusEnum
from api.utils.database import get_cluster_connection
from api.utils.requests_utils import dict_to_json
from api.utils.security import verify_token

with open("firebase_config.json") as config_file:
    config = json.load(config_file)

router = APIRouter()

pb = pyrebase.initialize_app(config)


@router.post("/register", response_model=BaseResponseModel[User])
async def signup(
    register_details: AuthRequest,
    cluster: MongoClient = Depends(get_cluster_connection),
):
    try:
        user = auth.verify_id_token(register_details.token)
    except Exception as e:
        raise BaseHTTPException(
            message="Error creating user: " + e,
            status=StatusEnum.FAILURE,
            status_code=400,
        )

    users_db = cluster["pocketmint"]["users"]
    if users_db.find_one({"_id": user["uid"]}):
        raise BaseHTTPException(
            message="User already exists!",
            status=StatusEnum.FAILURE,
            status_code=400,
        )

    user_data = {
        "_id": user.get("uid"),
        "username": user.get("name"),
        "email": user.get("email"),
        "profile_picture": user.get("picture"),
        "registered_at": datetime.now(),
        "last_logged_in": datetime.now(),
        "roles": ["user"],
    }

    users_db.insert_one(user_data)

    return JSONResponse(
        content=BaseResponseModel(
            status=StatusEnum.SUCCESS,
            message="Successfully created user",
            data={"user": dict_to_json(user_data)},
        ),
        status_code=200,
    )


@router.post("/login", response_model=BaseResponseModel[User])
async def login(
    login_details: AuthRequest,
    cluster: MongoClient = Depends(get_cluster_connection),
):
    try:
        user = auth.verify_id_token(login_details.token)
    except Exception as e:
        raise BaseHTTPException(
            message="An error occurred: " + e,
            status=StatusEnum.FAILURE,
            status_code=400,
        )

    # Update user in database
    user_db = cluster["pocketmint"]["users"]
    res = user_db.update_one(
        {"_id": user.get("uid")}, {"$set": {"last_logged_in": datetime.now()}}
    )
    if res.modified_count != 1:
        raise BaseHTTPException(
            message="User was not found in database.",
            status=StatusEnum.FAILURE,
            status_code=400,
        )

    # Find user in database
    user = user_db.find_one({"_id": user.get("uid")})

    return JSONResponse(
        content=BaseResponseModel(
            message="User logged in successfully!",
            status=StatusEnum.SUCCESS,
            data={"user": dict_to_json(user)},
        ),
        status_code=200,
    )


@router.post(
    "/profile_change_password",
    response_model=BaseResponseModel[GeneralResponse],
    dependencies=[Depends(verify_token)],
)
async def profile_change(profile_change_password_details: ProfileChangePasswordRequest):
    email, old_password, new_password, confirm_new_password = (
        profile_change_password_details.email,
        profile_change_password_details.old_password,
        profile_change_password_details.new_password,
        profile_change_password_details.confirm_new_password,
    )

    # Check if old password is correct
    try:
        user = pb.auth().sign_in_with_email_and_password(email, old_password)
    except requests.exceptions.HTTPError as e:
        error_message = json.loads(e.args[1]).get("error").get("message")
        if error_message == "INVALID_PASSWORD":
            raise BaseHTTPException(
                status_code=400,
                message="Provided old password is incorrect!",
                status=StatusEnum.FAILURE,
            )
        else:
            raise BaseHTTPException(
                message=GENERIC_EXCEPTION_MESSAGE,
                status=StatusEnum.FAILURE,
                status_code=400,
                data={"error": str(e)},
            )

    # Check if new password and confirm new password match
    if new_password != confirm_new_password:
        raise BaseHTTPException(
            message="Provided new passwords do not match!",
            status=StatusEnum.FAILURE,
            status_code=400,
        )

    # Update password
    try:
        auth.update_user(user.get("localId"), password=new_password)
    except Exception as e:
        raise BaseHTTPException(
            message=GENERIC_EXCEPTION_MESSAGE,
            status=StatusEnum.FAILURE,
            status_code=400,
            data={"error": str(e)},
        )

    return JSONResponse(
        content=BaseResponseModel(
            message="Successfully changed password!",
            status=StatusEnum.SUCCESS,
        ).dict(),
        status_code=200,
    )
