from core.exception import CoreUserIsNull, UserDontHasPermission

from database.logic.permission import check_user as check_user_permission
from database.client_db.database import Role
from database.client_db.requests import Role_IO, Signature, User_IO

def create(
    organization_id: int,
    role: dict,
    user: dict):

    if not check_user_permission(
        organization_id = organization_id,
        signature = f"0:0:2:4",
        user = user):
        raise UserDontHasPermission()
    
    signatures = []
    for perm in role["permission"]:
        if perm["accounts"] == None:
            signatures.append(
                Signature(
                    category_id = perm["category_id"],
                    account_id = 0,
                    move = perm["move"],
                    obj = perm["object"]
                )
            )
            continue

    Role_IO.create(
        organization_id = organization_id,
        name = role["name"],
        signatures = signatures
    )

def get_all(
    organization_id: int,
    user: dict):

    if not User_IO.inOrganization(
        organization_id,
        user):
        raise CoreUserIsNull()
    
    roles = [
        role.toJson() 
        for role in  Role_IO.get_all(
            organization_id = organization_id
        )
    ]

    return roles

def edit(
    organization_id: int,
    role_id: int,
    name: str,
    user: dict):

    if not check_user_permission(
        organization_id = organization_id,
        signature = f"0:0:4:4",
        user = user):
        raise UserDontHasPermission()
    
    Role_IO.edit_name(
        organization_id = organization_id,
        role_id = role_id,
        name = name
    )

def delete(
    organization_id: int,
    role_id: int,
    user: dict):

    if not check_user_permission(
        organization_id = organization_id,
        signature = f"0:0:3:4",
        user = user):
        raise UserDontHasPermission()
    
    Role_IO.delete(
        organization_id = organization_id,
        role_id = role_id
    )