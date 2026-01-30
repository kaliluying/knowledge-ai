"""
分类序列化器模块
"""

from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    分类序列化器（完整版）
    """

    parent_id = serializers.PrimaryKeyRelatedField(
        source="parent",
        queryset=Category.objects.all(),
        required=False,
        allow_null=True,
    )
    children_count = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "color",
            "icon",
            "parent",
            "parent_id",
            "owner",
            "is_active",
            "sort_order",
            "level",
            "children_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "owner", "created_at", "updated_at"]

    def get_children_count(self, obj):
        """获取子分类数量"""
        return obj.get_children().count()

    def get_level(self, obj):
        """获取层级"""
        return obj.level

    def validate_parent(self, value):
        """验证父分类"""
        if value and value.owner != self.context["request"].user:
            raise serializers.ValidationError("不能选择其他用户的分类作为父分类")
        return value


class CategoryListSerializer(serializers.ModelSerializer):
    """
    分类序列化器（精简版）
    """

    level = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "color",
            "icon",
            "parent",
            "is_active",
            "sort_order",
            "level",
        ]

    def get_level(self, obj):
        """获取层级"""
        return obj.level


class CategoryTreeSerializer(serializers.ModelSerializer):
    """
    分类树形序列化器

    递归嵌套子分类
    """

    children = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()
    children_count = serializers.SerializerMethodField()
    notes_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "color",
            "icon",
            "parent",
            "is_active",
            "sort_order",
            "level",
            "value",
            "label",
            "children",
            "children_count",
            "notes_count",
        ]

    def get_children(self, obj):
        """递归获取子分类"""
        children = obj.get_children()
        if children.exists():
            return CategoryTreeSerializer(children, many=True).data
        return []

    def get_level(self, obj):
        """获取层级"""
        return obj.level

    def get_value(self, obj):
        """获取值（用于下拉选择）"""
        return obj.id

    def get_label(self, obj):
        """获取标签（用于显示）"""
        prefix = "　" * obj.level
        return f"{prefix}{obj.name}"

    def get_children_count(self, obj):
        """获取子分类数量"""
        return obj.get_children().count()

    def get_notes_count(self, obj):
        """获取该分类下的笔记数量"""
        from apps.notes.models import Note
        # 直接使用 category_id 过滤，避免 MPTT 对象比较问题
        return Note.objects.filter(category_id=obj.id, is_archived=False).count()


class CategoryCreateSerializer(serializers.ModelSerializer):
    """
    分类创建序列化器
    """

    parent_id = serializers.PrimaryKeyRelatedField(
        source="parent",
        queryset=Category.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Category
        fields = [
            "name",
            "description",
            "color",
            "icon",
            "parent_id",
            "sort_order",
        ]

    def validate_parent_id(self, value):
        """验证父分类是否存在且属于当前用户"""
        if value and value.owner != self.context["request"].user:
            raise serializers.ValidationError("不能选择其他用户的分类")
        return value

    def create(self, validated_data):
        """创建分类"""
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


class CategoryUpdateSerializer(serializers.ModelSerializer):
    """
    分类更新序列化器
    """

    class Meta:
        model = Category
        fields = [
            "name",
            "description",
            "color",
            "icon",
            "parent",
            "is_active",
            "sort_order",
        ]

    def validate_parent(self, value):
        """验证父分类"""
        if value and value.owner != self.context["request"].user:
            raise serializers.ValidationError("不能选择其他用户的分类作为父分类")
        # 不能将分类设置为自己的子分类
        if value and value.id == self.instance.id:
            raise serializers.ValidationError("不能将分类设置为自己的子分类")
        return value
