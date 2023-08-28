from enum import Enum


# Insurance Categories
class InsuranceCategory(str, Enum):
    GENERAL = "General"
    HEALTH = "Health"
    LIFE = "Life"
    INVESTMENT = "Investment"


# Insurance Types
class LifeInsurance(str, Enum):
    TERM_LIFE = "Term Life"
    WHOLE_LIFE = "Whole Life"
    UNIVERSAL_LIFE = "Universal Life"


class InvestmentInsurance(str, Enum):
    ENDOWMENT = "Endowment"
    INVESTMENT_RELATED = "Investment Related"
    RETIREMENT = "Retirement"


class HealthInsurance(str, Enum):
    HOSPITALIZATION = "Hospitalization"
    CRITICAL_ILLNESS = "Critical Illness"
    PERSONAL_ACCIDENT = "Personal Accident"
    PRIVATE_INTEGRATED_SHIELD_PLANS = "Private Integrated Shield Plans"


class OthersInsurance(str, Enum):
    HELPER = "Helper"
    TRAVEL = "Travel"
    CAR = "Car"
    DISABILITY = "Disability"
    FURNITURE_AND_HOME_CONTENTS = "Furniture and Home Contents"
    GENERAL_BUILDING = "General Building"
    HOME_MORTGAGE = "Home Mortgage"


# Coverage Types
class CoverageType(str, Enum):
    OTHERS = "Others"
    TOTAL_PERMANENT_DISABILITY = "Total Permanent Disability"
    PERSONAL_ACCIDENT = "Personal Accident"
    HOSPITALIZATION_CHARGES = "Hospitalization Charges"
    GENERAL_BUILDING_RENOVATIONS = "General Building/Renovations"
    FURNITURE_HOME_CONTENT = "Furniture/Home Content"
    DISABILITY_HOSPITALIZATION_INCOME = "Disability/Hospitalization Income"
    CRITICAL_ILLNESS = "Critical Illness"
    DEATH = "Death"
