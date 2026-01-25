"""
笔记模块 URL 配置

API Endpoints:
- GET    /api/notes/           - 笔记列表
- POST   /api/notes/           - 创建笔记
- GET    /api/notes/{id}/      - 笔记详情
- PUT    /api/notes/{id}/      - 更新笔记
- DELETE /api/notes/{id}/      - 删除笔记
- POST   /api/notes/{id}/archive/   - 归档笔记
- POST   /api/notes/{id}/unarchive/ - 取消归档
- POST   /api/notes/{id}/pin/       - 置顶笔记
- GET    /api/notes/search/?q=关键词 - 搜索笔记
- GET    /api/notes/recent/         - 最近笔记
- GET    /api/notes/archived/       - 已归档笔记
- GET    /api/notes/{id}/content/   - 获取笔记内容
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet

app_name = "notes"

router = DefaultRouter()
router.register(r"", NoteViewSet, basename="note")

urlpatterns = [
    path("", include(router.urls)),
]
