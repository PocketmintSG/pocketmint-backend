import json
import pyrebase
from datetime import datetime
from fastapi.params import Depends
from firebase_admin import auth, db
from fastapi import APIRouter, UploadFile, File
from pymongo import MongoClient
import requests
from api.configs.constants.exceptions import (
    GENERIC_EXCEPTION_MESSAGE,
)
from api.models.request_models.auth import (
    AuthRequest,
    AuthRequestWithName,
    ProfileChangePasswordRequest,
    ProfileUpdateRequest,
)
from api.models.response_models.common import (
    BaseHTTPException,
    BaseJSONResponse,
    BaseResponseModel,
    GeneralResponse,
)
from api.models.user import User
from api.types.requests_types import StatusEnum
from api.utils.auth import get_user
from api.utils.database import get_cluster_connection
from api.utils.misc import dict_to_json
from api.utils.security import verify_token

# with open("firebase_config.json") as config_file:
# config = json.load(config_file)

router = APIRouter()

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


@router.post("/register", response_model=BaseResponseModel[User])
async def signup(
    register_details: AuthRequestWithName,
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
        "username": register_details.username,
        "first_name": register_details.first_name,
        "last_name": register_details.last_name,
        "email": user.get("email"),
        "profile_picture": user.get("picture"),
        "registered_at": datetime.now(),
        "last_logged_in": datetime.now(),
        "roles": ["user"],
    }

    users_db.insert_one(user_data)

    return BaseJSONResponse(
        status=StatusEnum.SUCCESS,
        message="Successfully created user",
        data={"user": dict_to_json(user_data)},
        status_code=200,
    )


@router.post("/login", response_model=BaseResponseModel[User])
async def login(
    login_details: AuthRequest,
    cluster: MongoClient = Depends(get_cluster_connection),
):
    try:
        user = auth.verify_id_token(login_details.token)
        uid = user.get("uid")
        user = auth.get_user(uid)
        revocation_second = user.tokens_valid_after_timestamp / 1000
        metadata_ref = db.reference("metadata/" + uid)
        metadata_ref.set({"revokeTime": revocation_second})
    except Exception as e:
        raise BaseHTTPException(
            message="An error occurred: " + str(e),
            status=StatusEnum.FAILURE,
            status_code=400,
        )

    # Update user in database
    user_db = cluster["pocketmint"]["users"]
    res = user_db.update_one({"_id": uid}, {"$set": {"last_logged_in": datetime.now()}})
    if res.modified_count != 1:
        raise BaseHTTPException(
            message="User was not found in database.",
            status=StatusEnum.FAILURE,
            status_code=400,
        )

    # Find user in database
    user = user_db.find_one({"_id": uid})

    return BaseJSONResponse(
        status=StatusEnum.SUCCESS,
        message="User logged in successfully!",
        data={"user": dict_to_json(user)},
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

    return BaseJSONResponse(
        status=StatusEnum.SUCCESS,
        message="Successfully changed password!",
    )


@router.post(
    "/update_profile",
    response_model=BaseResponseModel[GeneralResponse],
    dependencies=[Depends(verify_token)],
)
async def update_profile(
    details: ProfileUpdateRequest,
    cluster: MongoClient = Depends(get_cluster_connection),
):
    users_db = cluster["pocketmint"]["users"]
    details = details.dict()
    user_data = {
        "username": details.get("username"),
        "first_name": details.get("first_name"),
        "last_name": details.get("last_name"),
        "email": details.get("email"),
        "profile_picture": details.get("profile_picture_url"),
    }

    auth.update_user(
        details.get("uid"),
        display_name=details.get("username"),
        email=details.get("email"),
        photo_url=details.get("profile_picture_url"),
    )

    users_db.update_one({"_id": details.get("uid")}, {"$set": user_data})

    return BaseJSONResponse(
        message="Profile successfully updated!",
        status=StatusEnum.SUCCESS,
        data={"user": dict_to_json(get_user(details.get("uid")))},
    )
