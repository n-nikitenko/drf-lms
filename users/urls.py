from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (PaymentListApiView, UserCreateApiView,
                         UserDestroyApiView, UserListApiView,
                         UserRetrieveApiView, UserUpdateApiView)

app_name = UsersConfig.name

urlpatterns = [
    path("", UserListApiView.as_view(), name="users_list"),
    path("<int:pk>/", UserRetrieveApiView.as_view(), name="user_retrieve"),
    path("<int:pk>/update/", UserUpdateApiView.as_view(), name="user_update"),
    path("<int:pk>/delete/", UserDestroyApiView.as_view(), name="user_destroy"),
    path("payments/", PaymentListApiView.as_view(), name="payments_list"),
    path("register/", UserCreateApiView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=[AllowAny]),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=[AllowAny]),
        name="token_refresh",
    ),
]
