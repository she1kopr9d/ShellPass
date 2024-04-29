import json

from core.data_utils import AuthorizeRequest
from core.utils import AuthorizeRedirect, get_req_args, AuthorizePermissionRequest

from organization.models import Organization
from organization.logic.invite import create_invite_link
from organization.logic.database_server import PostInDatabase, database_url_start

from django.http import HttpRequest, HttpResponse

@AuthorizeRequest()
def organizationsList(
    request: HttpRequest,
    user: dict):

    organizations = Organization.objects.filter(
        creator_id = user["id"]
    )
    return HttpResponse(
        content = json.dumps(
            [
                org.toJson()
                for org in organizations
            ]
        )
    )

@AuthorizeRequest()
def createOrganization(
    request: HttpRequest,
    user: dict):

    name = get_req_args(
        "name",
        request = request
    )
    try:
        organization = Organization(
            name = name,
            creator_id = user["id"]
        )
        organization.save()
    except:
        return HttpResponse(
            content = "error"
        )
    
    req = PostInDatabase(
        url = f"database/create",
        body = {
            "organization_id" : organization.pk
        },
        request = request
    )
    
    return HttpResponse(
        content = "ok"
    )

@AuthorizeRedirect(
    url = f"{database_url_start}database/category/create",
    method = "POST"
)
def createCategory():
    pass

@AuthorizeRedirect(
    url = f"{database_url_start}database/account/create",
    method = "POST"
)
def createAccount():
    pass

@AuthorizeRedirect(
    url = f"{database_url_start}database/role/create",
    method = "POST"
)
def createRole():
    pass

@AuthorizeRedirect(
    url = f"{database_url_start}database/role/view_all",
    method = "GET"
)
def viewAllRole():
    pass
    
@AuthorizeRedirect(
    url = f"{database_url_start}database/role/edit",
    method = "POST"
)
def editRoleName():
    pass

@AuthorizeRedirect(
    url = f"{database_url_start}database/role/delete",
    method = "POST"
)
def deleteRole():
    pass

@AuthorizePermissionRequest(
        signature = "0:0:1:5"
)
def createInviteLink(
    request: HttpRequest,
    user: dict):
    
    organization_id, invite_type = get_req_args(
        "organization_id",
        "invite_type",
        request = request
    )
    try:
        link = create_invite_link(
            organization_id = organization_id,
            invite_type = invite_type,
            user = user
        )
    except:
        return HttpResponse(
            content = "Error"
        )
    return HttpResponse(
        content = json.dumps(
            {
                "link" : link
            }
        )
    )