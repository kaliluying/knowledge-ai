"""
附件序列化器模块
"""

from rest_framework import serializers
from .models import Attachment


class AttachmentSerializer(serializers.ModelSerializer):
    """附件详情序列化器"""

    size_formatted = serializers.ReadOnlyField()
    extension = serializers.ReadOnlyField()

    class Meta:
        model = Attachment
        fields = [
            "id",
            "name",
            "file",
            "file_type",
            "mime_type",
            "size",
            "size_formatted",
            "extension",
            "note",
            "created_at",
        ]
        read_only_fields = [
            "file_type",
            "mime_type",
            "size",
            "size_formatted",
            "extension",
            "created_at",
        ]


class AttachmentListSerializer(serializers.ModelSerializer):
    """附件列表序列化器（精简版）"""

    size_formatted = serializers.ReadOnlyField()

    class Meta:
        model = Attachment
        fields = [
            "id",
            "name",
            "file",
            "file_type",
            "size",
            "size_formatted",
            "created_at",
        ]


class AttachmentCreateSerializer(serializers.ModelSerializer):
    """附件创建序列化器"""

    class Meta:
        model = Attachment
        fields = [
            "name",
            "file",
            "note",
        ]

    def validate_file(self, value):
        """验证文件类型和大小"""
        # 最大文件大小: 50MB
        max_size = 50 * 1024 * 1024

        if value.size > max_size:
            raise serializers.ValidationError("文件大小不能超过 50MB")

        # 允许的文件类型（移除 SVG 防止 XSS 攻击）
        allowed_types = [
            "image/jpeg",
            "image/png",
            "image/gif",
            "image/webp",
            # "image/svg+xml",  # 已移除：SVG 可能包含恶意脚本
            "application/pdf",
            "text/plain",
            "text/markdown",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.ms-powerpoint",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            "video/mp4",
            "video/webm",
            "audio/mpeg",
            "audio/wav",
        ]

        content_type = value.content_type if value.content_type else ""

        if content_type and content_type not in allowed_types:
            raise serializers.ValidationError("不支持的文件类型")

        return value

    def create(self, validated_data):
        """创建附件"""
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)
