"""
附件视图模块
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Attachment
from .serializers import (
    AttachmentSerializer,
    AttachmentListSerializer,
    AttachmentCreateSerializer,
)


class AttachmentViewSet(viewsets.ModelViewSet):
    """
    附件视图集

    提供附件的 CRUD 操作
    """

    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        """获取当前用户的附件"""
        return Attachment.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        """根据动作返回不同的序列化器"""
        if self.action == "list":
            return AttachmentListSerializer
        if self.action == "create":
            return AttachmentCreateSerializer
        return AttachmentSerializer

    def perform_create(self, serializer):
        """创建时设置所有者"""
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """创建附件"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        attachment = serializer.save()

        output_serializer = AttachmentSerializer(attachment)
        return Response(
            {
                "code": 201,
                "message": "上传成功",
                "data": output_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def list(self, request, *args, **kwargs):
        """获取附件列表"""
        queryset = self.get_queryset()

        # 按笔记过滤
        note_id = request.query_params.get("note")
        if note_id:
            queryset = queryset.filter(note_id=note_id)

        # 按文件类型过滤
        file_type = request.query_params.get("type")
        if file_type:
            queryset = queryset.filter(file_type=file_type)

        # 排序
        order = request.query_params.get("order", "-created_at")
        queryset = queryset.order_by(order)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "code": 200,
                "message": "获取成功",
                "data": serializer.data,
                "count": queryset.count(),
            }
        )

    def retrieve(self, request, *args, **kwargs):
        """获取附件详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {
                "code": 200,
                "message": "获取成功",
                "data": serializer.data,
            }
        )

    def destroy(self, request, *args, **kwargs):
        """删除附件"""
        instance = self.get_object()

        # 删除文件
        if instance.file:
            instance.file.delete(save=False)

        instance.delete()
        return Response(
            {
                "code": 200,
                "message": "删除成功",
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"])
    def recent(self, request):
        """获取最近附件"""
        limit = int(request.query_params.get("limit", 10))
        attachments = self.get_queryset()[:limit]
        serializer = AttachmentListSerializer(attachments, many=True)
        return Response(
            {
                "code": 200,
                "message": "获取成功",
                "data": serializer.data,
            }
        )

    @action(detail=False, methods=["delete"])
    def bulk_delete(self, request):
        """批量删除附件"""
        ids = request.data.get("ids", [])

        if not ids:
            return Response(
                {"code": 400, "message": "请提供要删除的附件ID列表"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        attachments = self.get_queryset().filter(id__in=ids)

        for attachment in attachments:
            if attachment.file:
                attachment.file.delete(save=False)
            attachment.delete()

        return Response(
            {
                "code": 200,
                "message": f"成功删除 {len(ids)} 个附件",
            }
        )
