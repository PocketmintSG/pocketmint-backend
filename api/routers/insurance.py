from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends
from pymongo import MongoClient
from api.models.request_models.insurance import (
    DeleteInsuranceRequest,
    GetInsuranceSummariesRequest,
    ListInsuranceRequest,
    UpdateInsuranceRequest,
)

from api.models.response_models.common import (
    BaseHTTPException,
    BaseJSONResponse,
    BaseResponseModel,
)
from api.models.response_models.insurance import InsuranceModel, InsuranceModelMinified
from api.types.insurance import (
    OthersInsurance,
    HealthInsurance,
    InvestmentInsurance,
    LifeInsurance,
)
from api.types.requests_types import StatusEnum
from api.utils.database import get_cluster_connection
from api.utils.misc import dict_to_json, get_chunks, model_to_dict
from api.utils.security import verify_token

router = APIRouter()


@router.post(
    "/create_insurance",
    response_model=BaseResponseModel[InsuranceModel],
    dependencies=[Depends(verify_token)],
)
async def create_insurance(
    insurance_details: InsuranceModel,
    cluster: MongoClient = Depends(get_cluster_connection),
):
    insurance_db = cluster["pocketmint"]["insurance_details"]
    insurance_details = model_to_dict(insurance_details)
    res = insurance_db.insert_one(insurance_details)

    insurance_details["_id"] = str(res.inserted_id)

    return BaseJSONResponse(
        status=StatusEnum.SUCCESS,
        message="Insurance successfully created!",
        status_code=200,
        data=insurance_details,
    )


@router.get(
    "/get_insurance/{insurance_id}",
    response_model=BaseResponseModel[InsuranceModel],
    dependencies=[Depends(verify_token)],
)
async def read_insurance(
    insurance_id: str, cluster: MongoClient = Depends(get_cluster_connection)
):
    insurance_db = cluster["pocketmint"]["insurance_details"]
    res = insurance_db.find_one({"_id": ObjectId(insurance_id)})
    if not res:
        raise BaseHTTPException(
            status=StatusEnum.FAILURE,
            status_code=404,
            message="Insurance not found!",
        )

    return BaseJSONResponse(
        status=StatusEnum.SUCCESS,
        message="Insurance found!",
        status_code=200,
        data=dict_to_json(res),
    )


@router.post(
    "/list_insurance",
    response_model=BaseResponseModel[List[InsuranceModelMinified]],
    dependencies=[Depends(verify_token)],
)
async def list_insurance(
    insurance_details: ListInsuranceRequest,
    cluster: MongoClient = Depends(get_cluster_connection),
):
    """Returns the minimum information required to show insurance information. Only returns name, insurer, type, agent details, beneficiary, and insured by.

    When a user opens a table row as a collapsible, then the full information is fetched using the get_insurance endpoint.

    Filtering in the table is done in the frontend for now. Right now, we only allow users to filter by insurance name.
    """
    insurance_details = insurance_details.dict()
    insurance_db = cluster["pocketmint"]["insurance_details"]
    all_insurance = list(insurance_db.find({"uid": insurance_details["user_id"]}))
    res = []
    if all_insurance != None:
        # Extract the bare minimum information
        # Each insurance policy can contain one or more insurance coverage types. We will display a truncated list of all coverage types covered in each insurance policy.
        for insurance in all_insurance:
            res.append(
                {
                    "_id": str(insurance["_id"]),
                    "policy_name": insurance["policy_details"]["insurance_name"],
                    "policy_insurer": insurance["policy_details"]["insurer"],
                    "policy_insurance_types": list(
                        map(
                            lambda x: x["insurance_type"],
                            insurance["insurance_coverage"]["coverage_details"],
                        )
                    ),
                    "agent_name": insurance["agent_details"]["name"],
                    "agent_contact_number": insurance["agent_details"][
                        "contact_number"
                    ],
                    "agent_contact_number": insurance["agent_details"][
                        "contact_number"
                    ],
                    "beneficiary": insurance["policy_details"]["beneficiary"],
                    # "insured_by": insurance["policy_details"]["beneficiary"],
                }
            )

    # chunks = get_chunks(res, insurance_details["pagination_chunk_size"])
    return BaseJSONResponse(
        status=StatusEnum.SUCCESS,
        message="Insurance listed!",
        data=res,
    )


@router.post(
    "/update_insurance",
    response_model=BaseResponseModel[InsuranceModel],
    dependencies=[Depends(verify_token)],
)
async def update_insurance(
    insurance_details: UpdateInsuranceRequest,
    cluster: MongoClient = Depends(get_cluster_connection),
):
    details_dict = insurance_details.dict()
    insurance_db = cluster["pocketmint"]["insurance_details"]
    if not insurance_db.find_one({"_id": ObjectId(details_dict["insurance_id"])}):
        raise BaseHTTPException(
            status=StatusEnum.FAILURE,
            status_code=404,
            message="Insurance not found!",
        )
    res = model_to_dict(insurance_details)["updated_details"]
    insurance_db.update_one(
        {"_id": ObjectId(details_dict["insurance_id"])}, {"$set": res}
    )

    return BaseJSONResponse(
        status=StatusEnum.SUCCESS,
        message="Insurance updated!",
        status_code=200,
        data=res,
    )


@router.post(
    "/delete_insurance",
    response_model=BaseResponseModel[InsuranceModel],
    dependencies=[Depends(verify_token)],
)
async def delete_insurance(
    insurance_details: DeleteInsuranceRequest,
    cluster: MongoClient = Depends(get_cluster_connection),
):
    details_dict = insurance_details.dict()
    insurance_db = cluster["pocketmint"]["insurance_details"]
    deleted_insurance = insurance_db.find_one(
        {"_id": ObjectId(details_dict["insurance_id"])}
    )
    if not deleted_insurance:
        raise BaseHTTPException(
            status=StatusEnum.FAILURE,
            status_code=404,
            message="Insurance not found!",
        )

    insurance_db.delete_one({"_id": ObjectId(details_dict["insurance_id"])})
    return BaseJSONResponse(
        status=StatusEnum.SUCCESS,
        message="Insurance deleted!",
        status_code=200,
        data=deleted_insurance,
    )


@router.post(
    "/get_insurance_summaries",
    response_model=BaseResponseModel[InsuranceModel],
    dependencies=[Depends(verify_token)],
)
async def get_insurance_summaries(
    insurance_details: GetInsuranceSummariesRequest,
    cluster: MongoClient = Depends(get_cluster_connection),
):
    details_dict = insurance_details.dict()
    insurance_db = cluster["pocketmint"]["insurance_details"]
    user_insurances = list(insurance_db.find({"uid": details_dict["user_id"]}))

    total_annual_premiums = list(
        insurance_db.aggregate(
            [
                {
                    "$group": {
                        "_id": None,
                        "total_annual_premiums": {
                            "$sum": "$policy_details.cash_premiums"
                        },
                    }
                }
            ]
        )
    )

    # If DB is empty
    total_annual_premiums = (
        total_annual_premiums[0]["total_annual_premiums"]
        if len(total_annual_premiums) > 0
        else 0
    )

    data = {
        "insurance_coverage": {
            "total_annual_premiums": total_annual_premiums,
            "life": {
                "term": insurance_db.count_documents(
                    {
                        "uid": details_dict["user_id"],
                        "insurance_coverage.coverage_details.insurance_type": LifeInsurance.TERM_LIFE,
                    }
                )
                > 0,
                "whole_life": insurance_db.count_documents(
                    {
                        "uid": details_dict["user_id"],
                        "insurance_coverage.coverage_details.insurance_type": LifeInsurance.WHOLE_LIFE,
                    }
                )
                > 0,
                "universal_life": insurance_db.count_documents(
                    {
                        "uid": details_dict["user_id"],
                        "insurance_coverage.coverage_details.insurance_type": LifeInsurance.UNIVERSAL_LIFE,
                    }
                )
                > 0,
            },
            "accident_and_health": {
                "hospitalization": insurance_db.count_documents(
                    {
                        "uid": details_dict["user_id"],
                        "insurance_coverage.coverage_details.insurance_type": HealthInsurance.HOSPITALIZATION,
                    }
                )
                > 0,
                "critical_illness": insurance_db.count_documents(
                    {
                        "uid": details_dict["user_id"],
                        "insurance_coverage.coverage_details.insurance_type": HealthInsurance.CRITICAL_ILLNESS,
                    }
                )
                > 0,
                "personal_accident": insurance_db.count_documents(
                    {
                        "uid": details_dict["user_id"],
                        "insurance_coverage.coverage_details.insurance_type": HealthInsurance.PERSONAL_ACCIDENT,
                    }
                )
                > 0,
                "private_integrated_shield_plans": insurance_db.count_documents(
                    {
                        "uid": details_dict["user_id"],
                        "insurance_coverage.coverage_details.insurance_type": HealthInsurance.PRIVATE_INTEGRATED_SHIELD_PLANS,
                    }
                )
                > 0,
            },
            "investments": {
                "endowment": insurance_db.count_documents(
                    {
                        "uid": details_dict["user_id"],
                        "insurance_coverage.coverage_details.insurance_type": InvestmentInsurance.ENDOWMENT,
                    }
                )
                > 0,
                "investment_related": insurance_db.count_documents(
                    {
                        "uid": details_dict["user_id"],
                        "insurance_coverage.coverage_details.insurance_type": InvestmentInsurance.INVESTMENT_RELATED,
                    }
                )
                > 0,
                "retirement": insurance_db.count_documents(
                    {
                        "uid": details_dict["user_id"],
                        "insurance_coverage.coverage_details.insurance_type": InvestmentInsurance.RETIREMENT,
                    }
                )
                > 0,
            },
            "others": insurance_db.count_documents(
                {
                    "uid": details_dict["user_id"],
                    "insurance_coverage.coverage_details.insurance_type": {
                        "$in": [enum.value for enum in OthersInsurance]
                    },
                }
            )
            > 0,
        },
        "maximum_sum_insured": {
            "life": list(
                map(
                    lambda x: x["max_total_premiums"],
                    insurance_db.aggregate(
                        [
                            {
                                "$match": {
                                    "insurance_coverage.insurance_category": {
                                        "$in": ["Life"]
                                    }
                                }
                            },
                            {
                                "$group": {
                                    "_id": None,
                                    "max_total_premiums": {
                                        "$max": "$insurance_coverage.total_premiums"
                                    },
                                }
                            },
                        ]
                    ),
                )
            ),
            "accident_and_health": list(
                map(
                    lambda x: x["max_total_premiums"],
                    insurance_db.aggregate(
                        [
                            {
                                "$match": {
                                    "insurance_coverage.insurance_category": {
                                        "$in": ["Health"]
                                    }
                                }
                            },
                            {
                                "$group": {
                                    "_id": None,
                                    "max_total_premiums": {
                                        "$max": "$insurance_coverage.total_premiums"
                                    },
                                }
                            },
                        ]
                    ),
                )
            ),
            "investments": list(
                map(
                    lambda x: x["max_total_premiums"],
                    insurance_db.aggregate(
                        [
                            {
                                "$match": {
                                    "insurance_coverage.insurance_category": {
                                        "$in": ["Investment"]
                                    }
                                }
                            },
                            {
                                "$group": {
                                    "_id": None,
                                    "max_total_premiums": {
                                        "$max": "$insurance_coverage.total_premiums"
                                    },
                                }
                            },
                        ]
                    ),
                )
            ),
            "others": list(
                map(
                    lambda x: x["max_total_premiums"],
                    insurance_db.aggregate(
                        [
                            {
                                "$match": {
                                    "insurance_coverage.insurance_category": {
                                        "$in": ["Others"]
                                    }
                                }
                            },
                            {
                                "$group": {
                                    "_id": None,
                                    "max_total_premiums": {
                                        "$max": "$insurance_coverage.total_premiums"
                                    },
                                }
                            },
                        ]
                    ),
                )
            ),
        },
    }

    return BaseJSONResponse(
        status=StatusEnum.SUCCESS,
        message="Insurance summary retrieved!",
        status_code=200,
        data=data,
    )
