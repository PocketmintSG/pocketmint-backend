from typing import Any, Optional

from pydantic import BaseModel

from api.types.requests_types import StatusEnum


class ResponseBaseModel(BaseModel):
    status: StatusEnum
    message: str
    data: Optional[Any]
