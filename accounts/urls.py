# users/urls.py
from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", include("allauth.urls")),
    path('user/profile/', EmployeeProfileView.as_view(), name="user_profile"),
    path('user/index/',UserListView.as_view(), name="user-index"), 
    path('user/create/', register_user, name="user-create"),  
    path('user/password-reset/', reset_password, name="reset-password"),  
    path('user/update/<int:pk>/', UserUpdateView.as_view(), name="user-update"), 
    path('user/details/<int:pk>/', UserDetailView.as_view(), name="user-details"), 
    path('user/delete/<int:pk>/',UserDeleteView.as_view(), name="user-delete"), 
    path('logout/', custom_logout, name='logout'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'), name='password_reset_request'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name='password_reset_complete'),
    path('reset/', CustomPasswordResetView.as_view(), name='password_reset'),

    path("register/", RegisterUserView.as_view(), name="register_user"),
    path('login-modal/', login_modal, name='login_modal'),

    path(
        'facilitator-profile/update/<int:pk>/',
        FacilitatorProfileUpdateView.as_view(),
        name='facilitator-profile-update'
    ),
    path('profession/add/', profession_add, name='profession-add'),
    path('qualification/add/', qualification_add, name='qualification-add'),
]
