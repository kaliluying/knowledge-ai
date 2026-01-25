"""
标签视图模块
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Tag
from .serializers import (
    TagSerializer,
    TagListSerializer,
    TagCreateSerializer,
    TagUpdateSerializer,
)
from utils.permissions import IsOwnerOrReadOnly


class TagViewSet(viewsets.ModelViewSet):
    """
    标签视图集

    提供 CRUD 操作:
    - GET /api/tags/ - 标签列表
    - POST /api/tags/ - 创建标签
    - GET /api/tags/{id}/ - 标签详情
    - PUT /api/tags/{id}/ - 更新标签
    - DELETE /api/tags/{id}/ - 删除标签
    - GET /api/tags/hot/ - 热门标签
    - GET /api/tags/search/ - 搜索标签
    """

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "id"

    def get_queryset(self):
        """获取当前用户的标签"""
        user = self.request.user
        queryset = Tag.objects.filter(owner=user)

        # 搜索
        search = self.request.query_params.get("search", None)
        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset

    def get_serializer_class(self):
        """根据操作返回不同的序列化器"""
        if self.action == "list":
            return TagListSerializer
        if self.action == "create":
            return TagCreateSerializer
        if self.action in ["update", "partial_update"]:
            return TagUpdateSerializer
        return TagSerializer

    def perform_create(self, serializer):
        """创建时设置所有者"""
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=["get"])
    def hot(self, request):
        """
        获取热门标签

        GET /api/tags/hot/?limit=10
        """
        limit = int(request.query_params.get("limit", 10))
        hot_tags = self.get_queryset().order_by("-usage_count")[:limit]

        serializer = TagListSerializer(hot_tags, many=True)
        return Response(
            {
                "code": 200,
                "message": "获取成功",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"])
    def search(self, request):
        """
        搜索标签

        GET /api/tags/search/?q=关键词
        """
        query = request.query_params.get("q", "")
        if not query:
            return Response(
                {"code": 400, "message": "请提供搜索关键词"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tags = self.get_queryset().filter(name__icontains=query)[:20]

        serializer = TagListSerializer(tags, many=True)
        return Response(
            {
                "code": 200,
                "message": "获取成功",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"])
    def all(self, request):
        """
        获取所有标签

        GET /api/tags/all/
        """
        tags = self.get_queryset().order_by("name")

        serializer = TagListSerializer(tags, many=True)
        return Response(
            {
                "code": 200,
                "message": "获取成功",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"])
    def bulk_create(self, request):
        """
        批量创建标签

        POST /api/tags/bulk_create/
        Body: { "names": ["标签1", "标签2", "标签3"] }
        """
        names = request.data.get("names", [])
        if not names:
            return Response(
                {"code": 400, "message": "请提供标签名称列表"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        created_tags = []
        existing_tags = []

        for name in names:
            name = name.strip()
            if not name:
                continue

            # 检查是否已存在
            tag, created = Tag.objects.get_or_create(
                name=name,
                owner=request.user,
                defaults={"slug": Tag.objects.model(name=name).slug},
            )

            if created:
                created_tags.append(tag)
            else:
                existing_tags.append(tag)

        return Response(
            {
                "code": 201,
                "message": f"创建成功 {len(created_tags)} 个标签",
                "data": {
                    "created": TagListSerializer(created_tags, many=True).data,
                    "existing": TagListSerializer(existing_tags, many=True).data,
                },
            },
            status=status.HTTP_201_CREATED,
        )
