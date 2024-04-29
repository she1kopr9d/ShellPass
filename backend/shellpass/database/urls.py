from django.urls import path
from database.views import createDatabase, getUserPermission, createCategory, createAccount, createRole, viewAllRole, editRoleName, deleteRole, checkUserPermission

app_name = "database"

urlpatterns = [
    path('create', createDatabase),
    path('user/permission', getUserPermission),
    path('user/permission/check', checkUserPermission),
    path('category/create', createCategory),
    path('account/create', createAccount),
    path('role/create', createRole),
    path('role/view_all', viewAllRole),
    path('role/edit', editRoleName),
    path('role/delete', deleteRole),
]