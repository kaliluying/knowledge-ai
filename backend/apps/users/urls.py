"""
用户模块 URL 配置

API Endpoints:
- POST   /api/auth/register/       - 用户注册
- POST   /api/auth/login/          - 用户登录
- POST   /api/auth/logout/         - 用户登出
- POST   /api/auth/refresh/        - 刷新 Token
- GET    /api/auth/profile/        - 获取用户信息
- PUT    /api/auth/profile/        - 更新用户信息
- POST   /api/auth/password/       - 修改密码
- GET    /api/auth/users/{id}/     - 获取指定用户信息
- GET    /api/auth/preferences/    - 获取偏好设置
- PUT    /api/auth/preferences/    - 更新偏好设置
- GET    /api/auth/sessions/       - 获取登录设备
- DELETE /api/auth/sessions/{id}/  - 退出指定设备
- GET    /api/auth/storage/        - 获取存储统计
- GET    /api/auth/export/         - 导出用户数据
- DELETE /api/auth/account/        - 删除账户
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
    PreferencesView,
    SessionsView,
    StorageView,
    ExportView,
    DeleteAccountView,
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
    # 偏好设置
    path("preferences/", PreferencesView.as_view(), name="preferences"),
    # 登录设备管理
    path("sessions/", SessionsView.as_view(), name="sessions"),
    path("sessions/<str:session_id>/", SessionsView.as_view(), name="session-detail"),
    # 存储统计
    path("storage/", StorageView.as_view(), name="storage"),
    # 数据导出
    path("export/", ExportView.as_view(), name="export"),
    # 账户删除
    path("account/", DeleteAccountView.as_view(), name="delete-account"),
    # 用户详情
    path("users/<int:user_id>/", UserDetailView.as_view(), name="user-detail"),
]
