"""
笔记序列化器模块
"""

from rest_framework import serializers
from .models import Note
from apps.categories.serializers import CategoryListSerializer
from apps.tags.serializers import TagListSerializer


class NoteSerializer(serializers.ModelSerializer):
    """
    笔记序列化器（完整版）
    """

    category = CategoryListSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source="category",
        queryset=Note._meta.get_field("category").related_model.objects.all(),
        required=False,
        allow_null=True,
    )
    tags = TagListSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        source="tags",
        queryset=Note._meta.get_field("tags").related_model.objects.all(),
        required=False,
        many=True,
    )
    word_count = serializers.SerializerMethodField()
    reading_time = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "plain_text",
            "cover_image",
            "category",
            "category_id",
            "tags",
            "tag_ids",
            "owner",
            "is_pinned",
            "is_archived",
            "view_count",
            "word_count",
            "reading_time",
            "created_at",
            "updated_at",
            "archived_at",
        ]
        read_only_fields = [
            "id",
            "slug",
            "plain_text",
            "owner",
            "is_archived",
            "view_count",
            "word_count",
            "reading_time",
            "created_at",
            "updated_at",
            "archived_at",
        ]

    def get_word_count(self, obj):
        """获取字数"""
        return len(obj.plain_text.split()) if obj.plain_text else 0

    def get_reading_time(self, obj):
        """获取阅读时间"""
        words = len(obj.plain_text.split()) if obj.plain_text else 0
        return max(1, words // 200)


class NoteListSerializer(serializers.ModelSerializer):
    """
    笔记序列化器（精简版）
    """

    category_name = serializers.CharField(
        source="category.name", allow_null=True, read_only=True
    )
    tag_names = serializers.SerializerMethodField()
    plain_text = serializers.CharField(read_only=True)

    class Meta:
        model = Note
        fields = [
            "id",
            "title",
            "slug",
            "cover_image",
            "plain_text",
            "category_name",
            "tag_names",
            "is_pinned",
            "is_archived",
            "view_count",
            "created_at",
            "updated_at",
        ]

    def get_tag_names(self, obj):
        """获取标签名称列表"""
        return list(obj.tags.values_list("name", flat=True))


class NoteCreateSerializer(serializers.ModelSerializer):
    """
    笔记创建序列化器
    """

    category_id = serializers.PrimaryKeyRelatedField(
        source="category",
        queryset=Note._meta.get_field("category").related_model.objects.all(),
        required=False,
        allow_null=True,
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        source="tags",
        queryset=Note._meta.get_field("tags").related_model.objects.all(),
        required=False,
        many=True,
    )

    class Meta:
        model = Note
        fields = [
            "title",
            "content",
            "cover_image",
            "category_id",
            "tag_ids",
            "is_pinned",
        ]

    def create(self, validated_data):
        """创建笔记"""
        validated_data["owner"] = self.context["request"].user
        tags = validated_data.pop("tags", [])
        note = Note.objects.create(**validated_data)
        if tags:
            note.tags.set(tags)
        return note


class NoteUpdateSerializer(serializers.ModelSerializer):
    """
    笔记更新序列化器
    """

    category_id = serializers.PrimaryKeyRelatedField(
        source="category",
        queryset=Note._meta.get_field("category").related_model.objects.all(),
        required=False,
        allow_null=True,
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        source="tags",
        queryset=Note._meta.get_field("tags").related_model.objects.all(),
        required=False,
        many=True,
    )

    class Meta:
        model = Note
        fields = [
            "title",
            "content",
            "cover_image",
            "category_id",
            "tag_ids",
            "is_pinned",
        ]
