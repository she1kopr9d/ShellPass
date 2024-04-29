from core.exception import UserDontHasPermission

from database.client_db.database import Role
from database.client_db.requests import User_IO, Category_IO
from database.logic.permission import check_user as check_user_permission

def create(
    organization_id: int,
    category_name: str,
    user: dict):

    if not check_user_permission(
        organization_id = organization_id,
        signature = f"0:0:3:4",
        user = user):
        raise UserDontHasPermission()
    
    Category_IO.create(
        organization_id = organization_id,
        category_name = category_name
    )