from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any, TypeVar, Generic, Optional
from fastapi import HTTPException

from api.types.requests_types import StatusEnum

DataT = TypeVar("DataT")


class BaseResponseModel(BaseModel, Generic[DataT]):
    status: StatusEnum
    message: str
    data: Optional[DataT]


class GeneralResponse(BaseModel):
    data: Optional[Any]


class GeneralErrorResponse(BaseModel):
    error: str
    data: Optional[Any]


class BaseHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int,
        message: str,
        status: StatusEnum,
        data: Optional[GeneralErrorResponse] = None,
    ):
        super().__init__(
            status_code=status_code,
            detail=BaseResponseModel(message=message, status=status, data=data).dict(),
        )


class BaseJSONResponse(JSONResponse):
    def __init__(
        self,
        status: StatusEnum,
        message: str,
        data: Optional[GeneralResponse] = None,
        status_code: int = 200,
    ):
        super().__init__(
            content=BaseResponseModel(message=message, status=status, data=data).dict(),
            status_code=status_code,
        )
