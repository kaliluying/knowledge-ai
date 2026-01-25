"""
标签模块 URL 配置

API Endpoints:
- GET    /api/tags/           - 标签列表
- POST   /api/tags/           - 创建标签
- GET    /api/tags/{id}/      - 标签详情
- PUT    /api/tags/{id}/      - 更新标签
- DELETE /api/tags/{id}/      - 删除标签
- GET    /api/tags/hot/       - 热门标签
- GET    /api/tags/search/    - 搜索标签
- POST   /api/tags/bulk_create/ - 批量创建标签
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet

app_name = "tags"

router = DefaultRouter()
router.register(r"", TagViewSet, basename="tag")

urlpatterns = [
    path("", include(router.urls)),
]
