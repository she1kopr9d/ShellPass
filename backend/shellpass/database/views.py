import json

from core.utils import get_req_args
from core.exception import CoreUserIsNull, UserDontHasPermission
from core.data_utils import AuthorizeRequest

from database.logic.role import create as create_role
from database.logic.role import edit as edit_role_name
from database.logic.role import get_all as get_all_role
from database.logic.role import delete as delete_role
from database.logic.account import create as create_account
from database.logic.category import create as create_category
from database.logic.database import create as create_database
from database.logic.permission import check_user as check_user_permission
from database.client_db.requests import Utils_IO, User_IO, Category_IO, Account_IO, Signature, Role_IO

from django.http import HttpResponse, HttpRequest

@AuthorizeRequest()
def createDatabase(
    request: HttpRequest,
    user: dict):

    organization_id = get_req_args(
        "organization_id",
        request = request
    )

    create_database(
        organization_id = organization_id,
        user = user
    )

    return HttpResponse(
        content = "created"
    )

@AuthorizeRequest()
def getUserPermission(
    request: HttpRequest,
    user: dict):

    organization_id = get_req_args(
        "organization_id",
        request = request
    )

    permission = User_IO.get_user_permission(
        organization_id = organization_id,
        user = user
    )

    return HttpResponse(
        content = json.dumps(
            {
                "permission" : permission
            }
        )
    )

@AuthorizeRequest()
def checkUserPermission(
    request: HttpRequest,
    user: dict):

    organization_id, signature = get_req_args(
        "organization_id",
        "signature",
        request = request
    )
    answer = check_user_permission(
        organization_id = organization_id,
        signature = signature,
        user = user
    )

    return HttpResponse(
        content = json.dumps(
            {
                "can" : answer
            }
        )
    )

@AuthorizeRequest()
def createCategory(
    request: HttpRequest,
    user: dict):

    organization_id, category_name = get_req_args(
        "organization_id",
        "category_name",
        request = request
    )
    
    try:
        create_category(
            organization_id = organization_id,
            category_name = category_name,
            user = user
        )
    except UserDontHasPermission:
        return HttpResponse(
            content = "You don't have permission"
        )

    return HttpResponse(
        content = f"Category {category_name} has been created!"
    )

@AuthorizeRequest()
def createAccount(
    request: HttpRequest,
    user: dict):

    organization_id, category_id, account_name, site_link, login, email, password = get_req_args(
        "organization_id",
        "category_id",
        "account_name",
        "site_link",
        "login",
        "email",
        "password",
        request = request
    )
    
    try:
        create_account(
            organization_id = organization_id,
            category_id = category_id,
            account_name = account_name,
            site_link = site_link,
            login = login,
            email = email,
            password = password
        )
    except UserDontHasPermission:
        return HttpResponse(
            content = "You don't have permission"
        )
    
    return HttpResponse(
        content = f"Account has been created!"
    )
    

@AuthorizeRequest()
def createRole(
    request: HttpRequest,
    user: dict):

    organization_id, role = get_req_args(
        "organization_id",
        "role",
        request = request
    )
    
    try:
        create_role(
            organization_id = organization_id,
            role = role,
            user = user
        )
    except UserDontHasPermission:
        return HttpResponse(
            content = "You don't have permission"
        )
    
    return HttpResponse(
        content = f"Role {role["name"]} has been created!"
    )
    

@AuthorizeRequest()
def viewAllRole(
    request: HttpRequest,
    user: dict):

    organization_id = get_req_args(
        "organization_id",
        request = request
    )

    try:
        roles = get_all_role(
            organization_id = organization_id, 
            user = user
        )
    except CoreUserIsNull:
        return HttpResponse(
            content = "User is not a member organization"
        )

    return HttpResponse(
        content = json.dumps(
            ogj = roles
            )
        )

@AuthorizeRequest()
def editRoleName(
    request: HttpRequest,
    user: dict):

    organization_id, role_id, name = get_req_args(
        "organization_id",
        "role_id",
        "name",
        request = request
    )
    try:
        edit_role_name(
            organization_id = organization_id,
            role_id = role_id,
            name = name,
            user = user
        )
    except CoreUserIsNull:
        return HttpResponse(
            content = "User is not a member organization"
        )
    return HttpResponse(
        content = f"Role {name} has been created!"
    )

@AuthorizeRequest()
def deleteRole(
    request: HttpRequest,
    user: dict):

    organization_id, role_id = get_req_args(
        "organization_id",
        "role_id",
        request = request
    )

    try:
        delete_role(
            organization_id = organization_id,
            role_id = role_id,
            user = user
        )
    except CoreUserIsNull:
        return HttpResponse(
            content = "User is not a member organization"
        )
    
    return HttpResponse(
        content = f"Role has been deleted!"
    )