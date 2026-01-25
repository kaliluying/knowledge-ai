"""
用户模块 URL 配置
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = "users"

urlpatterns = [
    # 认证路由将在 Phase 3 中实现
    # path("register/", include("rest_registration.api.urls_register")),
    # path("login/", include("rest_registration.api.urls_login")),
    # path("logout/", include("rest_registration.api.urls_logout")),
]
