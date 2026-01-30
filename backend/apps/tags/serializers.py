"""
标签序列化器模块
"""

from rest_framework import serializers
from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    """
    标签序列化器（完整版）
    """

    usage_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
            "slug",
            "color",
            "description",
            "owner",
            "usage_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "slug",
            "owner",
            "created_at",
            "updated_at",
        ]

    def get_usage_count(self, obj):
        """获取使用次数"""
        return getattr(obj, "notes_count", obj.usage_count)


class TagListSerializer(serializers.ModelSerializer):
    """
    标签序列化器（精简版）
    """

    usage_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
            "slug",
            "color",
            "usage_count",
        ]

    def get_usage_count(self, obj):
        """获取使用次数"""
        return getattr(obj, "notes_count", obj.usage_count)


class TagCreateSerializer(serializers.ModelSerializer):
    """
    标签创建序列化器
    """

    class Meta:
        model = Tag
        fields = [
            "name",
            "color",
            "description",
        ]

    def create(self, validated_data):
        """创建标签"""
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


class TagUpdateSerializer(serializers.ModelSerializer):
    """
    标签更新序列化器
    """

    class Meta:
        model = Tag
        fields = [
            "name",
            "color",
            "description",
        ]

    def validate_name(self, value):
        """验证标签名称"""
        instance = self.instance
        if instance:
            # 检查是否有重复名称
            if (
                Tag.objects.filter(name=value, owner=instance.owner)
                .exclude(id=instance.id)
                .exists()
            ):
                raise serializers.ValidationError("该标签名称已存在")
        return value
