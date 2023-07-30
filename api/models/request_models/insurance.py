from pydantic import BaseModel


class ListInsuranceRequest(BaseModel):
    user_id: str
    pagination_chunk_size: int
