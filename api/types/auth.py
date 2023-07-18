from enum import Enum

from pydantic import BaseModel


class ActionsEnum(str, Enum):
    """Represents the actions available to act on a resource"""

    CREATE: "CREATE"
    READ: "READ"
    UPDATE: "UPDATE"
    DELETE: "DELETE"


class ResourcesEnum(str, Enum):
    """Temporary placeholder to represent the types of resource available"""

    AUTH: "AUTH"
    GENERAL: "GENERAL"
    INSURANCE: "INSURANCE"


class OrganizationRoles(str, Enum):
    """Represents the types of roles an organization can have.

    NOTE: Need to consider what if there are different kinds of organizations!"""

    USER: "USER"
    IA: "IA"
    ADMIN: "ADMIN"


class BaseResource(BaseModel):
    """Represents common attributes that all resources will have"""

    owner: str
    created_at: str
    updated_at: str
    deleted_at: str or None
    is_deleted: bool
