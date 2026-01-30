"""
笔记视图模块

Markdown 编辑器内容管理
"""

import re
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
from apps.graph.models import GraphNode, GraphLink


def extract_note_links(content):
    """
    从 Markdown 内容中提取笔记链接
    返回链接到的笔记 ID 列表
    """
    if not content:
        return []

    # 匹配 [Note Title](/notes/{id}) 格式
    pattern = r'\[([^\]]+)\]\(/notes/(\d+)\)'
    matches = re.findall(pattern, content)

    note_ids = []
    for title, note_id in matches:
        try:
            note_ids.append(int(note_id))
        except ValueError:
            continue

    return note_ids


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
        """创建时设置所有者并建立笔记关联"""
        note = serializer.save(owner=self.request.user)
        # 提取内容中的笔记链接并建立关联
        self._update_related_notes(note)

    def _update_related_notes(self, note):
        """从笔记内容中提取链接并更新关联关系"""
        content = note.content
        if not content:
            # 清空关联时也需要清理图谱数据
            self._sync_graph_data(note, [])
            return

        # 提取内容中的笔记链接
        linked_note_ids = extract_note_links(content)

        # 获取用户的所有笔记
        user_notes = Note.objects.filter(owner=note.owner)

        # 过滤出有效的笔记 ID
        valid_note_ids = list(
            user_notes.filter(id__in=linked_note_ids).values_list("id", flat=True)
        )

        # 移除指向自己的链接
        valid_note_ids = [id for id in valid_note_ids if id != note.id]

        # 更新关联关系
        note.related_notes.set(valid_note_ids)

        # 双向关联：更新被关联的笔记
        for related_id in valid_note_ids:
            related_note = user_notes.filter(id=related_id).first()
            if related_note:
                related_note.related_notes.add(note)
                related_note.save(update_fields=[])

        # 清理不再关联的笔记的双向关系
        current_related = set(note.related_notes.values_list("id", flat=True))
        target_related = set(valid_note_ids)
        to_remove = current_related - target_related
        for removed_id in to_remove:
            removed_note = user_notes.filter(id=removed_id).first()
            if removed_note:
                removed_note.related_notes.remove(note)
                removed_note.save(update_fields=[])

        # 同步创建 GraphNode 和 GraphLink
        self._sync_graph_data(note, valid_note_ids)

    def _sync_graph_data(self, note, related_note_ids):
        """同步图谱数据：确保笔记节点存在并创建/删除链接"""
        user = note.owner

        # 确保当前笔记有 GraphNode
        note_node, _ = GraphNode.objects.get_or_create(
            owner=user,
            node_type="note",
            title=note.title,
            defaults={"label": note.title[:50]},
        )

        # 收集需要创建的链接目标节点
        target_nodes = {}

        for related_id in related_note_ids:
            related_note = Note.objects.filter(id=related_id, owner=user).first()
            if not related_note:
                continue

            # 确保关联笔记有 GraphNode
            related_node, _ = GraphNode.objects.get_or_create(
                owner=user,
                node_type="note",
                title=related_note.title,
                defaults={"label": related_note.title[:50]},
            )
            target_nodes[related_id] = related_node

        # 清理不再相关的 GraphLink
        GraphLink.objects.filter(
            owner=user,
            source=note_node,
            link_type="reference",
        ).exclude(
            target_id__in=list(target_nodes.keys())
        ).delete()

        # 创建新的 GraphLink
        for related_id, related_node in target_nodes.items():
            self._create_graph_link(user, note_node, related_node, "reference")

    def _create_graph_link(self, user, source_node, target_node, link_type):
        """创建图谱链接（如果不存在）"""
        if source_node.id == target_node.id:
            return

        GraphLink.objects.get_or_create(
            owner=user,
            source=source_node,
            target=target_node,
            defaults={"link_type": link_type},
        )

    def create(self, request, *args, **kwargs):
        """创建笔记并返回包装的响应"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # 获取完整的笔记数据
        note = Note.objects.get(id=serializer.instance.id)
        response_serializer = NoteSerializer(note)

        return Response(
            {
                "code": 201,
                "message": "创建成功",
                "data": response_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, request, *args, **kwargs):
        """获取笔记详情并返回包装的响应"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {
                "code": 200,
                "message": "获取成功",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        """更新笔记并返回包装的响应"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # 更新关联关系
        note = Note.objects.get(id=instance.id)
        self._update_related_notes(note)

        response_serializer = NoteSerializer(note)

        return Response(
            {
                "code": 200,
                "message": "更新成功",
                "data": response_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        """删除笔记"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "code": 200,
                "message": "删除成功",
            },
            status=status.HTTP_200_OK,
        )

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
    def suggestions(self, request):
        """
        获取笔记建议列表（用于内部链接选择）

        GET /api/notes/suggestions/?q=关键词
        返回 {id, title} 格式的简洁列表
        """
        query = request.query_params.get("q", "")
        limit = int(request.query_params.get("limit", 20))

        notes = self.get_queryset().filter(is_archived=False)

        if query:
            notes = notes.filter(title__icontains=query)

        notes = notes.order_by("-created_at")[:limit]

        # 返回简洁格式
        data = [{"id": note.id, "title": note.title} for note in notes]
        return Response(
            {
                "code": 200,
                "message": "获取成功",
                "data": data,
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
