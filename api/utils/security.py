from fastapi import HTTPException, Header
from fastapi.params import Header
from firebase_admin import auth

from starlette.status import HTTP_403_FORBIDDEN


async def verify_token(auth_token: str = Header(...)):
    """Verifies if the ID token passed in the header of a request is valid.

    NOTE: The request is expected to have a header called 'auth-token'."""
    if not auth_token:
        raise HTTPException(status_code=400, detail="Invalid headers provided")
    credentials_exception = HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Invalid credentials provided."
    )
    try:
        auth.verify_id_token(auth_token)
    except auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Credentials have expired."
        )
    except auth.RevokedIdTokenError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="User needs to reauthenticate."
        )
    except Exception as e:
        raise credentials_exception
