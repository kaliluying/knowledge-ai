"""
知识图谱模块 URL 配置
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GraphNodeViewSet, GraphLinkViewSet, GraphDataView, GraphRelatedView

app_name = "graph"

router = DefaultRouter()
router.register(r"nodes", GraphNodeViewSet, basename="node")
router.register(r"links", GraphLinkViewSet, basename="link")

urlpatterns = [
    path("graph/", GraphDataView.as_view(), name="graph-data"),
    path("related/<int:node_id>/", GraphRelatedView.as_view(), name="graph-related"),
    path("", include(router.urls)),
]
