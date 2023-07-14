from fastapi import HTTPException, Header
from fastapi.params import Header
from firebase_admin import auth

from starlette.status import HTTP_403_FORBIDDEN


async def verify_token(Auth_Token: str = Header(...)):
    """Verifies if the ID token passed in the header of a request is valid.

    NOTE: The request is expected to have a header called 'auth_token'."""
    if not Auth_Token:
        raise HTTPException(status_code=400, detail="Invalid headers provided")
    credentials_exception = HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Invalid credentials provided."
    )
    try:
        auth.verify_id_token(Auth_Token)
    except Exception as e:
        raise credentials_exception
