"""
知识图谱视图模块

提供图谱数据获取、节点管理、链接管理等 API 视图。
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import models

from .models import GraphNode, GraphLink
from .serializers import (
    GraphNodeSerializer,
    GraphLinkSerializer,
    GraphLinkCreateSerializer,
)
from .services import get_graph_data, get_related_graph_data
from utils.responses import ResponseModel


class GraphDataView(APIView):
    """
    图谱数据视图

    GET /api/graph/graph/
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        payload = get_graph_data(request.user)
        return Response(
            ResponseModel.success(data=payload).to_dict(),
            status=status.HTTP_200_OK,
        )


class GraphRelatedView(APIView):
    """
    相关图谱数据视图

    GET /api/graph/related/{id}/
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, node_id: int):
        payload = get_related_graph_data(request.user, node_id)
        return Response(
            ResponseModel.success(data=payload).to_dict(),
            status=status.HTTP_200_OK,
        )


class GraphNodeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    图谱节点视图集（只读）

    提供节点查询功能
    """

    queryset = GraphNode.objects.all()
    serializer_class = GraphNodeSerializer

    def get_queryset(self):
        """根据用户过滤节点"""
        user = self.request.user
        return GraphNode.objects.filter(owner=user)

    @action(detail=False, methods=["get"])
    def by_type(self, request):
        """
        按类型获取节点

        GET /api/graph/nodes/by_type/?type=note
        """
        node_type = request.query_params.get("type")
        if node_type:
            nodes = self.get_queryset().filter(node_type=node_type)
        else:
            nodes = self.get_queryset()

        serializer = self.get_serializer(nodes, many=True)
        return Response(ResponseModel.success(data=serializer.data).to_dict())


class GraphLinkViewSet(viewsets.ModelViewSet):
    """
    图谱链接视图集

    提供链接的创建、查询、删除等功能
    """

    queryset = GraphLink.objects.all()
    serializer_class = GraphLinkSerializer

    def get_queryset(self):
        """根据用户过滤链接"""
        user = self.request.user
        return GraphLink.objects.filter(owner=user)

    def get_serializer_class(self):
        """根据操作返回不同的序列化器"""
        if self.action == "create":
            return GraphLinkCreateSerializer
        return GraphLinkSerializer

    def create(self, request, *args, **kwargs):
        """
        创建图谱链接

        POST /api/graph/links/
        {
            "source": 1,
            "target": 2,
            "link_type": "related",
            "description": "相关笔记"
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 验证源节点和目标节点存在且属于当前用户
        source_id = serializer.validated_data.get("source")
        target_id = serializer.validated_data.get("target")

        source = get_object_or_404(GraphNode, id=source_id, owner=request.user)
        target = get_object_or_404(GraphNode, id=target_id, owner=request.user)

        # 验证链接不存在
        existing_link = GraphLink.objects.filter(
            owner=request.user,
            source=source,
            target=target,
        ).first()

        if existing_link:
            return Response(
                ResponseModel.error(message="链接已存在", code=400).to_dict(),
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 创建链接
        link = GraphLink.objects.create(
            owner=request.user,
            source=source,
            target=target,
            link_type=serializer.validated_data.get("link_type", "related"),
            description=serializer.validated_data.get("description"),
        )

        return Response(
            ResponseModel.created(data=GraphLinkSerializer(link).data).to_dict(),
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request, *args, **kwargs):
        """
        删除图谱链接

        DELETE /api/graph/links/{id}/
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            ResponseModel.success(message="删除成功").to_dict(),
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"])
    def by_node(self, request):
        """
        获取与指定节点相关的所有链接

        GET /api/graph/links/by_node/?node_id=1
        """
        node_id = request.query_params.get("node_id")
        if not node_id:
            return Response(
                ResponseModel.error(message="缺少 node_id 参数").to_dict(),
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 获取以该节点为源或目标的链接
        links = self.get_queryset().filter(
            models.Q(source_id=node_id) | models.Q(target_id=node_id)
        )

        serializer = self.get_serializer(links, many=True)
        return Response(ResponseModel.success(data=serializer.data).to_dict())

    @action(detail=False, methods=["delete"])
    def batch_delete(self, request):
        """
        批量删除链接

        DELETE /api/graph/links/batch_delete/
        {
            "link_ids": [1, 2, 3]
        }
        """
        link_ids = request.data.get("link_ids", [])
        if not link_ids:
            return Response(
                ResponseModel.error(message="缺少 link_ids 参数").to_dict(),
                status=status.HTTP_400_BAD_REQUEST,
            )

        deleted_count = self.get_queryset().filter(id__in=link_ids).delete()[0]

        return Response(
            ResponseModel.success(
                data={"deleted_count": deleted_count},
                message=f"成功删除 {deleted_count} 个链接",
            ).to_dict(),
            status=status.HTTP_200_OK,
        )
