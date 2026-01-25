"""
分类模块 URL 配置

API Endpoints:
- GET    /api/categories/           - 分类列表
- POST   /api/categories/           - 创建分类
- GET    /api/categories/{id}/      - 分类详情
- PUT    /api/categories/{id}/      - 更新分类
- DELETE /api/categories/{id}/      - 删除分类
- GET    /api/categories/tree/      - 分类树
- GET    /api/categories/root/      - 一级分类
- GET    /api/categories/all/      - 所有分类（扁平）
- GET    /api/categories/{id}/children/ - 子分类列表
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet

app_name = "categories"

router = DefaultRouter()
router.register(r"", CategoryViewSet, basename="category")

urlpatterns = [
    path("", include(router.urls)),
]
