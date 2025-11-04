from django.urls import path
from ..views.auth import RegisterUserView, LoginUserView

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
]
