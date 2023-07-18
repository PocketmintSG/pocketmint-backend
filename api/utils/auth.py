from typing import List
from api.models.response_models.auth import Role
from api.models.user import User
from api.types.auth import ActionsEnum, OrganizationRoles, ResourcesEnum


def is_allowed(
    actor: User,
    action: ActionsEnum,
    resource: ResourcesEnum,
):
    roles = get_org_role(actor)
    resource_owner_uid = get_owner_uid(resource)
    if OrganizationRoles.ADMIN in roles:
        # Always return True for admin
        return True

    # if not (Role(roles).is_permitted_action(roles)):
    #     # If the action is not permitted by the Role, return False
    #     return False

    if is_owner(actor, resource):
        # If the actor is the owner of the resource, they can do anything they want
        return True

    if (OrganizationRoles.IA in roles) and (
        is_same_organization(resource_owner_uid, actor["uid"])
    ):
        # If the actor is an IA and they're acting on the same resource as a User
        return True

    return False


def is_owner(actor: User, resource: ResourcesEnum):
    """Returns True if a resource is created by the actor.

    TODO: Implement when adding insurance ReBAC.
    """
    # return db.find_one({"_id": resource.get("_id")}) == actor["_id"]
    return True


def get_owner_uid(resource: ResourcesEnum) -> str:
    """Returns the UID of the resource"""
    pass


def get_org_role(actor: User) -> List[str]:
    """Returns the organization role of the actor"""
    # return user_db.find_one({"_id": actor.get("_id")})["roles"]
    pass


def is_same_organization(resource_owner_uid: str, actor_uid: str):
    """Returns True if an IA has a User in their organization"""
    return True
