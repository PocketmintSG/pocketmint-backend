from pydantic import BaseModel
from typing import List, TypeVar, Generic, Optional

DataT = TypeVar("DataT")


class BaseErrorModel(BaseModel):
    message: str
    status: Optional[str]


class BaseResponseModel(BaseModel, Generic[DataT]):
    status: str
    message: str
    data: Optional[DataT]
    errors: Optional[List[BaseErrorModel]]


class GeneralResponse(BaseModel):
    message: str
