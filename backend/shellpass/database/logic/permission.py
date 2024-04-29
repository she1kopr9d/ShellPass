from database.client_db.database import Role
from database.client_db.requests import User_IO

def check_user(
    organization_id: int,
    signature: str,
    user: dict):

    return Role.check(
        mainsign = signature, 
        signs = User_IO.get_user_permission(
            organization_id = organization_id, 
            user = user
        )
    )