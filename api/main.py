import uvicorn
import firebase_admin
import pyrebase
import json

from firebase_admin import credentials, auth
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from mangum import Mangum
from .utils.test_routes import utils_router

cred = credentials.Certificate(
    {
        "type": "service_account",
        "project_id": "pocketmint-backend",
        "private_key_id": "29ad10abd862720a699d3ce01b29499589965509",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCvjYixfO9KvIju\n2NE/hKwwi3HKADLI0JwjYMdNQh8aD+Bh43nlH/f5WKDHYBmuiLdkUP91k4sCOVbI\nKejfe60unG6Jo8byJyyicXQFydN4emahjN46xoEHGCa0kwHP+ofdAaqwK+WWFxcj\n1rM7V8SMwGwDQkhgDae8M7FfMszpdqBnTTgTvp+Wi7saN/YzTKyvRKMez5Pl3ein\nYJWnTI5h9r3cvY55dvTTYdraf13XX0jFlY0ZFen1Rp1XvW9RMV8sh9/97bJs0VJE\n9S6nc23s5IUmWAeCDV49RgXCNsrucwxSFbmS5ZiN9iKSJrsWbtL0lwtl1Ytv41+v\n6KIExxdjAgMBAAECggEAAd+tW1OdjDsp7P60cQyd9+CtJL5OzHTpjbkdN3ZitZkA\nyJqwdOEb+PXYtXgRnhrIdlIk/+DExY/OHNHRsfz0csBpr59nYrNHVy6F0f/++VS5\nHrVNs+vlealo1FmTVeBzLck0RLAbQbhaX2ANxq7foq71GC3PbvMGXMxicsUsibtd\nXVYiXkCC3xOzzKzfvT9cdaQwuWIIXkprjPSpde+BIeEOnGTpc3bDO+SrgebdvyDW\n9yl6QgB6U76TCS8de/f4stByutA/l8dCcAmOPgCYXY3ho2+RXlPJ5ylL+N7uaZHr\nQf61H9N6IrBXTI5atxoAxaUcKGxYHQnnA0gYvh29VQKBgQDmiJbE1kTL2hUwdY+W\nkdQBrsWmeXtqJ0c5n+a0LOgDCuAzYC1ViWVGt18lDyDYHXM+IfVx3lDU7Lvrp5oV\n1KVcWRFlfO4v71/5anxVwBOR4ua/f3hPjg5WDaSiahuQD+RXUrzjHqZZ6XCDrzho\nMMDVXvdvpIpHq0Bl6FYEPdBGBwKBgQDC8hwd05Hvs3g70fmmxMBSzQWIPR1blPHe\npsfdO9Lcckiu60M9vatRRwxDCOY+up9V2LZ10OqoQdpfzENPkxIUeKWsXSP1ZYZ+\nn41sMBSEVUq9TSJl1Hb82+6PYgXmVBjtBfKA/Ikvk7IXVIKgruLrmPXeKuCRw4hs\nchPL/sgsxQKBgQCuqAUyE/QDTbKICElFFi69J6BvQ9KQ1jlMGy06jFsrEu5Rfiha\nicHFFeBrv05u7cEF7cx6/KfY6ZJmM5C1wWmW0ZQwg7ohbwYTfO2+OcuZ14Jiyzxn\naYTLBYMZ2bIQLzocPn8Ew4/cxtOLsRDXPziZb12fo9Vv/vrHOoMQq5RDuQKBgQCn\nabXdo2iLWiuh67OilQq40Nq0Yg+JK4L++2leQ1bU+8wRc3Z+Whj6prIQC193dVsK\nJR6kVPJ/5nW7mTYg6yM2s1lLiX0s67Axo6GWzD+CWaDiqpAktO4uPk1DkyGP6J6z\nRk04mibR1du2D1xS032KaASVc2sBotLQlrMLl9SeJQKBgQDDwZErRNLhOJ5s44rY\nCQYq7E9eXfpQa+gHec230MnICNgbnto/Iv4OCTiO/XFwF94sVaiigH3ML0o0RVIm\nRr2bvTH3hi/XSvnnKnVtu7RC5aivdC6pmou1BEoDCCvwLhZe1pVVxGvCSDNTYO53\nFRFZjGTDnHj8HGXdOu7eKM3TSg==\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-pbu36@pocketmint-backend.iam.gserviceaccount.com",
        "client_id": "105639292448250919759",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-pbu36%40pocketmint-backend.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com",
    }
)
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(
    {
        "apiKey": "AIzaSyDe2EL4mshzuCsQoA9moiNv3uQZmkxLGXg",
        "authDomain": "pocketmint-backend.firebaseapp.com",
        "projectId": "pocketmint-backend",
        "storageBucket": "pocketmint-backend.appspot.com",
        "messagingSenderId": "49057279925",
        "appId": "1:49057279925:web:a396421a9a99ba056ef3fc",
        "measurementId": "G-PWTJ312C5M",
        "databaseURL": "https://pocketmint-backend-default-rtdb.asia-southeast1.firebasedatabase.app/",
    }
)

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


# login endpoint
@app.post("/login")
async def login(request: Request):
    req_json = await request.json()
    email = req_json["email"]
    password = req_json["password"]
    try:
        user = pb.auth().sign_in_with_email_and_password(email, password)
        jwt = user["idToken"]
        return JSONResponse(content={"token": jwt}, status_code=200)
    except:
        return HTTPException(
            detail={"message": "There was an error logging in"}, status_code=400
        )


# ping endpoint
@app.post("/ping")
async def validate(request: Request):
    headers = request.headers
    jwt = headers.get("authorization")
    print(f"jwt:{jwt}")
    user = auth.verify_id_token(jwt)
    return user["uid"]


# if __name__ == "__main__":
#     uvicorn.run("main:app")

handler = Mangum(app=app)
