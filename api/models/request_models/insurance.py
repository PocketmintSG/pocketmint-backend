from pydantic import BaseModel

from api.models.response_models.insurance import InsuranceModel


class ListInsuranceRequest(BaseModel):
    user_id: str
    # pagination_chunk_size: int


class UpdateInsuranceRequest(BaseModel):
    user_id: str
    insurance_id: str
    updated_details: InsuranceModel


class DeleteInsuranceRequest(BaseModel):
    user_id: str
    insurance_id: str


class GetInsuranceSummariesRequest(BaseModel):
    user_id: str
