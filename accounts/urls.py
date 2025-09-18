# users/urls.py
from django.urls import path
from .views import (
    RegisterUserView,
    UserListView,
    UserDetailView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    login_modal
)

urlpatterns = [
    path("", UserListView.as_view(), name="user_list"),
    path("create/", UserCreateView.as_view(), name="user_create"),
    path("<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("<int:pk>/update/", UserUpdateView.as_view(), name="user_update"),
    path("<int:pk>/delete/", UserDeleteView.as_view(), name="user_delete"),

    path("register/", RegisterUserView.as_view(), name="register_user"),
    path('login-modal/', login_modal, name='login_modal'),
]
