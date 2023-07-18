from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

DataT = TypeVar("DataT")


class BaseResponseModel(BaseModel, Generic[DataT]):
    status: str
    message: str
    data: Optional[DataT]
