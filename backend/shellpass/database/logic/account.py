from core.exception import UserDontHasPermission

from database.client_db.database import Role
from database.client_db.requests import Account_IO, User_IO
from database.logic.permission import check_user as check_user_permission

def create(
    organization_id: int,
    category_id: int,
    account_name: str,
    site_link: str,
    login: str,
    email: str,
    password: str,
    user: dict):
    
    if not check_user_permission(
        organization_id = organization_id,
        signature = f"0:0:3:4",
        user = user):
        raise UserDontHasPermission()

    Account_IO.create(
        organization_id = organization_id,
        category_id = category_id,
        account_name = account_name,
        site_link = site_link,
        login = login,
        email = email,
        password = password)