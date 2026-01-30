"""
知识图谱序列化器模块
"""

from rest_framework import serializers
from .models import GraphNode, GraphLink


class GraphNodeSerializer(serializers.ModelSerializer):
    """图谱节点序列化器"""

    class Meta:
        model = GraphNode
        fields = [
            "id",
            "node_type",
            "title",
            "label",
            "data",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class GraphLinkSerializer(serializers.ModelSerializer):
    """图谱链接序列化器"""

    source = GraphNodeSerializer(read_only=True)
    target = GraphNodeSerializer(read_only=True)
    source_id = serializers.IntegerField(write_only=True, required=False)
    target_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = GraphLink
        fields = [
            "id",
            "source",
            "target",
            "source_id",
            "target_id",
            "link_type",
            "description",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class GraphLinkCreateSerializer(serializers.Serializer):
    """图谱链接创建序列化器"""

    source = serializers.IntegerField(
        required=True,
        help_text="源节点 ID",
    )
    target = serializers.IntegerField(
        required=True,
        help_text="目标节点 ID",
    )
    link_type = serializers.ChoiceField(
        choices=GraphLink.LINK_TYPE_CHOICES,
        default="related",
        help_text="链接类型",
    )
    description = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True,
        help_text="链接描述",
    )


class GraphDataSerializer(serializers.Serializer):
    """图谱数据序列化器"""

    nodes = GraphNodeSerializer(many=True)
    links = GraphLinkSerializer(many=True)
