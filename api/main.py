from fastapi.params import Depends
import firebase_admin

from firebase_admin import credentials, auth
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from mangum import Mangum
from api.models.auth import LoginRequest
from api.utils.security import verify_token
from api.utils.test_routes import utils_router

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

app.include_router(utils_router, prefix="/utils", tags=["utils"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


# signup endpoint
@app.post("/signup")
async def signup(request: Request):
    req = await request.json()
    email = req["email"]
    password = req["password"]
    if email is None or password is None:
        return HTTPException(
            detail={"message": "Error! Missing Email or Password"}, status_code=400
        )
    try:
        user = auth.create_user(email=email, password=password)
        return JSONResponse(
            content={"message": f"Successfully created user {user.uid}"},
            status_code=200,
        )
    except:
        return HTTPException(detail={"message": "Error Creating User"}, status_code=400)


@app.post("/login")
async def login(loginDetails: LoginRequest):
    try:
        user = auth.verify_id_token(loginDetails.token)
        return JSONResponse(content={"token": "Hello world"}, status_code=200)
    except Exception as e:
        return HTTPException(detail={"message": e}, status_code=400)


# ping endpoint
@app.post("/ping", dependencies=[Depends(verify_token)])
async def validate():
    return JSONResponse(content={"message": "Pong!"}, status_code=200)


handler = Mangum(app=app)
