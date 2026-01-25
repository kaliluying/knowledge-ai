"""
用户模块 URL 配置

API Endpoints:
- POST   /api/auth/register/     - 用户注册
- POST   /api/auth/login/        - 用户登录
- POST   /api/auth/logout/       - 用户登出
- POST   /api/auth/refresh/      - 刷新 Token
- GET    /api/auth/profile/      - 获取用户信息
- PUT    /api/auth/profile/      - 更新用户信息
- POST   /api/auth/password/     - 修改密码
- GET    /api/auth/users/{id}/   - 获取指定用户信息
"""

from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    RefreshTokenView,
    ProfileView,
    ChangePasswordView,
    UserDetailView,
)

app_name = "users"

urlpatterns = [
    # 认证相关
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh"),
    # 用户信息
    path("profile/", ProfileView.as_view(), name="profile"),
    path("password/", ChangePasswordView.as_view(), name="password"),
    # 用户详情
    path("users/<int:user_id>/", UserDetailView.as_view(), name="user-detail"),
]
