import firebase_admin
import json

from fastapi.params import Depends
from firebase_admin import credentials
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api.configs.constants.auth import API_ROUTER_PREFIX
from api.utils.security import verify_token
from api.routers.router import api_router
from mangum import Mangum


with open("firebase_secrets.json") as json_file:
    cert = json.load(json_file)

cred = credentials.Certificate(cert)

firebase = firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://pocketmint-frontend-default-rtdb.asia-southeast1.firebasedatabase.app/"
    },
)

app = FastAPI()
allow_all = ["*"]
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=allow_all,
    allow_headers=allow_all,
)

app.include_router(api_router, prefix=API_ROUTER_PREFIX, tags=["api"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


# ping endpoint
@app.post("/ping", dependencies=[Depends(verify_token)])
async def validate():
    return JSONResponse(content={"message": "Pong!"}, status_code=200)


handler = Mangum(app=app)
