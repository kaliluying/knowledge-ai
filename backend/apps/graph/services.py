"""
知识图谱服务模块

提供图谱数据组装与相关节点查询等服务。
"""

from django.db.models import Q

from .models import GraphNode, GraphLink


def _serialize_node(node: object) -> dict[str, object]:
    raw_data = getattr(node, "data", {}) or {}
    data = raw_data if isinstance(raw_data, dict) else {}
    created_at = getattr(node, "created_at", None)
    created_at_value = None
    if created_at is not None and hasattr(created_at, "isoformat"):
        created_at_value = created_at.isoformat()
    payload: dict[str, object] = {
        "id": getattr(node, "id", None),
        "name": getattr(node, "label", None) or getattr(node, "title", ""),
        "type": getattr(node, "node_type", ""),
        "value": data.get("value", 1),
        "created_at": created_at_value,
    }

    if "category" in data:
        payload["category"] = data.get("category")
    if "tags" in data:
        payload["tags"] = data.get("tags")

    return payload


def _serialize_link(link: object) -> dict[str, object]:
    """序列化链接，返回 source/target 为数字ID（兼容前端格式）"""
    return {
        "id": getattr(link, "id", None),
        "source": getattr(link, "source_id", None),
        "target": getattr(link, "target_id", None),
        "type": getattr(link, "link_type", ""),
        "strength": 1,
    }


def get_graph_data(user: object) -> dict[str, list[dict[str, object]]]:
    """
    获取完整图谱数据

    Returns:
        {"nodes": [...], "links": [...]} 的字典
    """
    nodes = GraphNode.objects.filter(owner=user)
    links = GraphLink.objects.filter(owner=user)

    return {
        "nodes": [_serialize_node(node) for node in nodes],
        "links": [_serialize_link(link) for link in links],
    }


def get_related_graph_data(
    user: object, node_id: int
) -> dict[str, list[dict[str, object]]]:
    """
    获取指定节点相关的节点与链接

    Returns:
        {"nodes": [...], "links": [...]} 的字典
    """
    links = GraphLink.objects.filter(owner=user).filter(
        Q(source_id=node_id) | Q(target_id=node_id)
    )

    node_ids = {node_id}
    for link in links:
        source_id = getattr(link, "source_id", None)
        target_id = getattr(link, "target_id", None)
        if source_id is not None:
            node_ids.add(int(source_id))
        if target_id is not None:
            node_ids.add(int(target_id))

    nodes = GraphNode.objects.filter(owner=user, id__in=node_ids)

    return {
        "nodes": [_serialize_node(node) for node in nodes],
        "links": [_serialize_link(link) for link in links],
    }
