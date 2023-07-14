from datetime import datetime
from fastapi.params import Depends
import firebase_admin

from firebase_admin import credentials, auth
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from mangum import Mangum
from pymongo import MongoClient
from api.models.auth import AuthRequest
from api.models.requests_models import BaseResponseModel
from api.models.user import User
from api.types.requests_types import StatusEnum
from api.utils.database import get_cluster_connection
from api.utils.requests_utils import dict_to_json
from api.utils.security import verify_token

import json

with open("firebase_secrets.json") as json_file:
    cert = json.load(json_file)

cred = credentials.Certificate(cert)

firebase = firebase_admin.initialize_app(cred)

app = FastAPI()
allow_all = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_all,
    allow_credentials=True,
    allow_methods=allow_all,
    allow_headers=allow_all,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/register", response_model=BaseResponseModel[User])
async def signup(
    register_details: AuthRequest,
    cluster: MongoClient = Depends(get_cluster_connection),
):
    try:
        user = auth.verify_id_token(register_details.token)
    except Exception as e:
        return HTTPException(
            detail={
                "message": "Error creating user: " + e,
                "status": StatusEnum.FAILURE,
            },
            status_code=400,
        )

    users_db = cluster["pocketmint"]["users"]
    if users_db.find_one({"_id": user["uid"]}):
        raise HTTPException(
            detail={"message": "User already exists!", "status": StatusEnum.FAILURE},
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
        content={
            "status": StatusEnum.SUCCESS,
            "message": "Successfully created user",
            "data": {"user": dict_to_json(user_data)},
        },
        status_code=200,
    )


@app.post("/login", response_model=BaseResponseModel[User])
async def login(
    login_details: AuthRequest,
    cluster: MongoClient = Depends(get_cluster_connection),
):
    try:
        user = auth.verify_id_token(login_details.token)
    except Exception as e:
        return HTTPException(
            detail={"message": "An error occurred: " + e, "status": StatusEnum.FAILURE},
            status_code=400,
        )

    # Update user in database
    user_db = cluster["pocketmint"]["users"]
    res = user_db.update_one(
        {"_id": user.get("uid")}, {"$set": {"last_logged_in": datetime.now()}}
    )
    if res.modified_count != 1:
        raise HTTPException(
            detail={
                "message": "User was not found in database.",
                "status": StatusEnum.FAILURE,
            },
            status_code=400,
        )

    # Find user in database
    user = user_db.find_one({"_id": user.get("uid")})

    return JSONResponse(
        content={
            "message": "User logged in successfully!",
            "status": StatusEnum.SUCCESS,
            "data": {"user": dict_to_json(user)},
        },
        status_code=200,
    )


# ping endpoint
@app.post("/ping", dependencies=[Depends(verify_token)])
async def validate():
    return JSONResponse(content={"message": "Pong!"}, status_code=200)


handler = Mangum(app=app)
