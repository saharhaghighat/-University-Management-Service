from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from account.views import UserRegistrationView, CustomLogoutView

app_name = "account"

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("users/login/", TokenObtainPairView.as_view(), name="user_login"),
    path("users/register/", UserRegistrationView.as_view(), name="user_register"),
    path('users/logout/', CustomLogoutView.as_view(), name='custom_logout'),

]
