from django.urls import path
from organization.views import createOrganization, organizationsList, createCategory, createAccount, createRole, viewAllRole, editRoleName, deleteRole, createInviteLink

app_name = "organization"

urlpatterns = [
    path('create', createOrganization),
    path('view', organizationsList),
    path('category/create', createCategory),
    path('account/create', createAccount),
    path('role/create', createRole),
    path('role/view_all', viewAllRole),
    path('role/edit', editRoleName),
    path('role/delete', deleteRole),
    path('user/create/invite', createInviteLink)
    #path('refresh-token', CookieTokenRefreshView.as_view()),
]
