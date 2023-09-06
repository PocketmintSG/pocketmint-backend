from fastapi import HTTPException, Header
from fastapi.params import Header
from firebase_admin import auth

from starlette.status import HTTP_403_FORBIDDEN

from api.models.response_models.common import BaseHTTPException
from api.types.requests_types import StatusEnum


async def verify_token(authorization: str = Header(...)):
    """Verifies if the ID token passed in the header of a request is valid."""

    if not authorization:
        raise BaseHTTPException(
            status_code=400,
            message="Invalid headers provided",
            status=StatusEnum.FAILURE,
        )
    try:
        auth.verify_id_token(authorization.split(" ")[1])
    except auth.ExpiredIdTokenError:
        raise BaseHTTPException(
            status_code=401,
            message="Credentials has expired",
            status=StatusEnum.FAILURE,
        )
    except auth.RevokedIdTokenError:
        raise BaseHTTPException(
            status_code=400,
            message="User needs to reauthenticate",
            status=StatusEnum.FAILURE,
        )
    except Exception as e:
        raise BaseHTTPException(
            status_code=400,
            message="An error occurred: " + str(e),
            status=StatusEnum.FAILURE,
        )
