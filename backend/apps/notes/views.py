"""
笔记视图模块

TipTap 编辑器内容管理
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.utils import timezone

from .models import Note
from .serializers import (
    NoteSerializer,
    NoteListSerializer,
    NoteCreateSerializer,
    NoteUpdateSerializer,
)
from utils.permissions import IsOwnerOrReadOnly
from utils.pagination import NotePagination


class NoteViewSet(viewsets.ModelViewSet):
    """
    笔记视图集

    提供 CRUD 操作:
    - GET /api/notes/ - 笔记列表
    - POST /api/notes/ - 创建笔记
    - GET /api/notes/{id}/ - 笔记详情
    - PUT /api/notes/{id}/ - 更新笔记
    - DELETE /api/notes/{id}/ - 删除笔记
    - POST /api/notes/{id}/archive/ - 归档笔记
    - POST /api/notes/{id}/unarchive/ - 取消归档
    - GET /api/notes/search/ - 搜索笔记
    - GET /api/notes/recent/ - 最近笔记
    """

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "id"
    pagination_class = NotePagination

    def get_queryset(self):
        """获取当前用户的笔记"""
        user = self.request.user
        queryset = (
            Note.objects.filter(owner=user)
            .select_related("category")
            .prefetch_related("tags")
        )

        # 过滤归档状态
        is_archived = self.request.query_params.get("archived")
        if is_archived is not None:
            is_archived = is_archived.lower() in ("true", "1", "yes")
            queryset = queryset.filter(is_archived=is_archived)
        else:
            # 默认显示未归档的笔记
            queryset = queryset.filter(is_archived=False)

        # 过滤分类
        category_id = self.request.query_params.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # 过滤标签
        tag_id = self.request.query_params.get("tag")
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)

        # 排序
        order = self.request.query_params.get("order", "-created_at")
        if order == "title":
            queryset = queryset.order_by("title")
        elif order == "-title":
            queryset = queryset.order_by("-title")
        elif order == "view_count":
            queryset = queryset.order_by("view_count")
        elif order == "-view_count":
            queryset = queryset.order_by("-view_count")
        else:
            queryset = queryset.order_by("-is_pinned", "-created_at")

        return queryset

    def get_serializer_class(self):
        """根据操作返回不同的序列化器"""
        if self.action == "list":
            return NoteListSerializer
        if self.action == "create":
            return NoteCreateSerializer
        if self.action in ["update", "partial_update"]:
            return NoteUpdateSerializer
        return NoteSerializer

    def perform_create(self, serializer):
        """创建时设置所有者"""
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"])
    def archive(self, request, id=None):
        """
        归档笔记

        POST /api/notes/{id}/archive/
        """
        note = self.get_object()
        note.is_archived = True
        note.archived_at = timezone.now()
        note.save(update_fields=["is_archived", "archived_at"])

        return Response(
            {
                "code": 200,
                "message": "归档成功",
                "data": NoteSerializer(note).data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def unarchive(self, request, id=None):
        """
        取消归档

        POST /api/notes/{id}/unarchive/
        """
        note = self.get_object()
        note.is_archived = False
        note.archived_at = None
        note.save(update_fields=["is_archived", "archived_at"])

        return Response(
            {
                "code": 200,
                "message": "取消归档成功",
                "data": NoteSerializer(note).data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def pin(self, request, id=None):
        """
        置顶笔记

        POST /api/notes/{id}/pin/
        """
        note = self.get_object()
        note.is_pinned = not note.is_pinned
        note.save(update_fields=["is_pinned"])

        return Response(
            {
                "code": 200,
                "message": "置顶成功" if note.is_pinned else "取消置顶成功",
                "data": NoteSerializer(note).data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"])
    def search(self, request):
        """
        搜索笔记（全文搜索）

        GET /api/notes/search/?q=关键词
        """
        query = request.query_params.get("q", "")
        if not query:
            return Response(
                {"code": 400, "message": "请提供搜索关键词"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 全文搜索
        notes = (
            self.get_queryset()
            .filter(
                Q(title__icontains=query)
                | Q(plain_text__icontains=query)
                | Q(tags__name__icontains=query)
            )
            .distinct()
        )

        page = self.paginate_queryset(notes)
        if page is not None:
            serializer = NoteListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = NoteListSerializer(notes, many=True)
        return Response(
            {
                "code": 200,
                "message": "搜索成功",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"])
    def recent(self, request):
        """
        获取最近笔记

        GET /api/notes/recent/?limit=10
        """
        limit = int(request.query_params.get("limit", 10))
        notes = (
            self.get_queryset()
            .filter(is_archived=False)
            .order_by("-created_at")[:limit]
        )

        serializer = NoteListSerializer(notes, many=True)
        return Response(
            {
                "code": 200,
                "message": "获取成功",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"])
    def archived(self, request):
        """
        获取已归档笔记

        GET /api/notes/archived/
        """
        notes = self.get_queryset().filter(is_archived=True).order_by("-archived_at")

        page = self.paginate_queryset(notes)
        if page is not None:
            serializer = NoteListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = NoteListSerializer(notes, many=True)
        return Response(
            {
                "code": 200,
                "message": "获取成功",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["get"])
    def content(self, request, id=None):
        """
        获取笔记内容（仅内容字段）

        GET /api/notes/{id}/content/
        """
        note = self.get_object()
        return Response(
            {
                "code": 200,
                "message": "获取成功",
                "data": {"content": note.content},
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="increment-view")
    def increment_view(self, request, id=None):
        """
        增加浏览次数

        POST /api/notes/{id}/increment-view/
        """
        note = self.get_object()
        note.increment_view()
        return Response(
            {
                "code": 200,
                "message": "浏览次数已更新",
                "data": {"view_count": note.view_count},
            },
            status=status.HTTP_200_OK,
        )
