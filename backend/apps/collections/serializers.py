"""
收藏序列化器模块
"""

from rest_framework import serializers
from .models import Collection


class CollectionSerializer(serializers.ModelSerializer):
    """收藏详情序列化器"""

    reading_time = serializers.ReadOnlyField()
    domain = serializers.ReadOnlyField()

    class Meta:
        model = Collection
        fields = [
            "id",
            "title",
            "description",
            "url",
            "domain",
            "favicon",
            "image",
            "content",
            "is_processed",
            "word_count",
            "reading_time",
            "view_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "domain",
            "is_processed",
            "word_count",
            "reading_time",
            "view_count",
            "created_at",
            "updated_at",
        ]


class CollectionListSerializer(serializers.ModelSerializer):
    """收藏列表序列化器（精简版）"""

    reading_time = serializers.ReadOnlyField()

    class Meta:
        model = Collection
        fields = [
            "id",
            "title",
            "description",
            "url",
            "domain",
            "favicon",
            "image",
            "is_processed",
            "word_count",
            "reading_time",
            "created_at",
        ]


class CollectionCreateSerializer(serializers.ModelSerializer):
    """收藏创建序列化器"""

    class Meta:
        model = Collection
        fields = [
            "title",
            "description",
            "url",
            "favicon",
            "image",
        ]

    def validate_url(self, value):
        """验证 URL 格式"""
        from django.core.validators import URLValidator
        from django.core.exceptions import ValidationError

        validator = URLValidator()
        try:
            validator(value)
        except ValidationError:
            raise serializers.ValidationError("请输入有效的 URL 地址")

        return value

    def create(self, validated_data):
        """创建收藏"""
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)
