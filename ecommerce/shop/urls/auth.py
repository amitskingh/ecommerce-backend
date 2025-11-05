from django.urls import path
from ..views.auth import (
    RegisterUserView,
    LoginUserView,
    PasswordResetRequestView,
    ResetPasswordView,
)

urlpatterns = [
    path(
        "auth/register/",
        RegisterUserView.as_view(),
        name="register_user",
    ),
    path(
        "auth/login/",
        LoginUserView.as_view(),
        name="login_user",
    ),
    path(
        "auth/password-reset-request/",
        PasswordResetRequestView.as_view(),
        name="password_reset_request",
    ),
    path(
        "auth/password-reset/<str:token>/",
        ResetPasswordView.as_view(),
        name="password_reset",
    ),
]
