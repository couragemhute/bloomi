from django.urls import path
from role.views import (
    RoleCreateView,
    RoleDeleteView,
    RoleListView,
    RoleUpdateView,
    RoleDetailsView,
    RemoveRolePermissionDeleteView,
    
    PermissionListView,

)


urlpatterns = [
    path('roles-index', RoleListView.as_view(), name="role-list"),
    path('role-create/', RoleCreateView.as_view(), name="role-create"),
    path('update-role/<int:pk>/', RoleUpdateView.as_view(), name="role-update"),
    path('role-details/<int:pk>/', RoleDetailsView.as_view(), name="role-details"),
    path('create-role/<int:pk>/', RoleDeleteView.as_view(), name="role-delete"),
    path('remove-role-permission/<int:pk>/<int:role_pk>/', RemoveRolePermissionDeleteView.as_view(), name="remove-role-permission"),

    path('permissions/', PermissionListView.as_view(), name="permission-list"),

]