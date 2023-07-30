import datetime
from typing import List, Union
from pydantic import BaseModel

from api.types.insurance import (
    CoverageType,
    GeneralInsurance,
    HealthInsurance,
    InvestmentInsurance,
    LifeInsurance,
)


class CoverageDetail(BaseModel):
    insurance_type: Union[
        GeneralInsurance, LifeInsurance, InvestmentInsurance, HealthInsurance
    ]
    coverage_type: CoverageType
    coverage_amount: float


class InsuranceModelPolicyDetails(BaseModel):
    policy_number: str
    cash_premiums: float
    insurance_name: str
    insured_person: str
    insurer: str
    beneficiary: str
    maturity_date: datetime.datetime


class InsuranceModelInsuranceCoverage(BaseModel):
    cash_premiums: float
    insurance_type: str
    non_cash_premiums: float
    total_premiums: float
    coverage_details: List[CoverageDetail]


class InsuranceModelAgentDetails(BaseModel):
    name: str
    contact_number: str
    email: str
    agency: str


class InsuranceModelDescription(BaseModel):
    desc_text: str
    files: List[str]  # List of file URLs stored on AWS S3 bucket


class InsuranceModel(BaseModel):
    uid: str
    policy_details: InsuranceModelPolicyDetails
    insurance_coverage: InsuranceModelInsuranceCoverage
    agent_details: InsuranceModelAgentDetails
    description: InsuranceModelDescription
