"""
知识图谱服务模块

提供图谱数据组装与相关节点查询等服务。
"""

import re
from django.db.models import Q

from .models import GraphNode, GraphLink
from apps.notes.models import Note
from apps.categories.models import Category
from apps.tags.models import Tag


# 正则表达式匹配笔记链接格式: [标题](/notes/123)
NOTE_LINK_PATTERN = re.compile(r'\[([^\]]+)\]\\(/notes/(\d+)\\)')


def _serialize_node(node: object) -> dict[str, object]:
    raw_data = getattr(node, "data", {}) or {}
    data = raw_data if isinstance(raw_data, dict) else {}
    created_at = getattr(node, "created_at", None)
    created_at_value = None
    if created_at is not None and hasattr(created_at, "isoformat"):
        created_at_value = created_at.isoformat()

    # 获取原始ID（如果是同步数据）
    original_id = getattr(node, "original_id", None)

    payload: dict[str, object] = {
        "id": getattr(node, "id", None),
        "original_id": original_id,
        "name": getattr(node, "label", None) or getattr(node, "title", ""),
        "type": getattr(node, "node_type", ""),
        "source": getattr(node, "source", "manual"),
        "is_locked": getattr(node, "is_locked", False),
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


def get_hybrid_graph_data(user: object, mode: str = "hybrid") -> dict[str, list[dict[str, object]]]:
    """
    获取混合模式图谱数据

    聚合笔记、分类、标签表的同步数据与手动创建的GraphNode数据

    Args:
        user: 当前用户
        mode: 数据模式
            - "hybrid": 混合数据（默认）
            - "sync_only": 仅同步数据
            - "manual_only": 仅手动节点

    Returns:
        {"nodes": [...], "links": [...]} 的字典
    """
    nodes = []
    links = []
    id_mapping = {}  # 映射 (type, original_id) -> node_id (字符串格式)

    # 1. 同步模式或混合模式：获取笔记节点（优化：使用 select_related 和 prefetch_related 避免 N+1）
    if mode in ("hybrid", "sync_only"):
        notes = Note.objects.filter(owner=user, is_archived=False).select_related("category").prefetch_related("tags")
        for note in notes:
            # 使用字符串格式的 ID：note-{original_id}
            node_id = f"note-{note.id}"

            # 获取关联的分类
            category_name = None
            if note.category:
                category_name = note.category.name

            # 获取关联的标签
            tag_names = list(note.tags.values_list("name", flat=True))

            node = type("NoteNode", (), {
                "id": node_id,
                "original_id": note.id,
                "node_type": "note",
                "title": note.title,
                "label": note.title[:50],
                "data": {
                    "value": min(100, max(10, len(note.plain_text) // 100)),
                    "category": category_name,
                    "tags": tag_names,
                },
                "source": "sync",
                "is_locked": False,
                "created_at": note.created_at,
            })()

            nodes.append(node)
            id_mapping[("note", note.id)] = node_id

        # 2. 同步模式或混合模式：获取分类节点
        categories = Category.objects.filter(owner=user, is_active=True)
        for category in categories:
            node_id = f"category-{category.id}"

            node = type("CategoryNode", (), {
                "id": node_id,
                "original_id": category.id,
                "node_type": "category",
                "title": category.name,
                "label": category.name[:50],
                "data": {
                    "value": min(80, max(10, category.notes.count() * 10)),
                    "path": category.path,
                },
                "source": "sync",
                "is_locked": False,
                "created_at": category.created_at,
            })()

            nodes.append(node)
            id_mapping[("category", category.id)] = node_id

        # 3. 同步模式或混合模式：获取标签节点
        tags = Tag.objects.filter(owner=user)
        for tag in tags:
            node_id = f"tag-{tag.id}"

            node = type("TagNode", (), {
                "id": node_id,
                "original_id": tag.id,
                "node_type": "tag",
                "title": tag.name,
                "label": f"标签: {tag.name}"[:50],
                "data": {
                    "value": min(60, max(5, tag.usage_count * 5)),
                },
                "source": "sync",
                "is_locked": False,
                "created_at": tag.created_at,
            })()

            nodes.append(node)
            id_mapping[("tag", tag.id)] = node_id

    # 4. 手动模式或混合模式：获取手动创建的GraphNode
    if mode in ("hybrid", "manual_only"):
        manual_nodes = GraphNode.objects.filter(owner=user, source="manual")
        for node in manual_nodes:
            nodes.append(node)

    # 5. 构建链接关系（仅同步数据）
    if mode in ("hybrid", "sync_only"):
        # 笔记 -> 分类链接
        notes = Note.objects.filter(owner=user, is_archived=False).select_related("category")
        for note in notes:
            if note.category:
                note_node_id = id_mapping.get(("note", note.id))
                category_node_id = id_mapping.get(("category", note.category.id))
                if note_node_id and category_node_id:
                    link = type("Link", (), {
                        "id": f"note-{note.id}-cat-{note.category.id}",
                        "source_id": note_node_id,
                        "target_id": category_node_id,
                        "link_type": "parent",
                    })()
                    links.append(link)

        # 笔记 -> 标签链接
        note_tags = Note.objects.filter(owner=user, is_archived=False).prefetch_related("tags")
        for note in note_tags:
            note_node_id = id_mapping.get(("note", note.id))
            if note_node_id:
                for tag in note.tags.all():
                    tag_node_id = id_mapping.get(("tag", tag.id))
                    if tag_node_id:
                        link = type("Link", (), {
                            "id": f"note-{note.id}-tag-{tag.id}",
                            "source_id": note_node_id,
                            "target_id": tag_node_id,
                            "link_type": "tagged",
                        })()
                        links.append(link)

        # 笔记 -> 笔记链接（解析笔记内容中的内部链接）
        all_notes = Note.objects.filter(owner=user, is_archived=False)
        for note in all_notes:
            note_node_id = id_mapping.get(("note", note.id))
            if not note_node_id:
                continue

            # 解析内容中的链接
            content = note.content or ""
            matches = NOTE_LINK_PATTERN.findall(content)

            for matched_title, linked_note_id in matches:
                linked_note_id = int(linked_note_id)
                linked_node_id = id_mapping.get(("note", linked_note_id))

                if linked_node_id:
                    # 避免重复链接
                    link_id = f"note-{note.id}-note-{linked_note_id}"
                    if not any(getattr(lnk, "id", None) == link_id for lnk in links):
                        link = type("Link", (), {
                            "id": link_id,
                            "source_id": note_node_id,
                            "target_id": linked_node_id,
                            "link_type": "references",
                        })()
                        links.append(link)

        # 笔记 -> 笔记链接（通过 related_notes 手动关联）
        related_notes = Note.objects.filter(owner=user, is_archived=False).prefetch_related("related_notes")
        for note in related_notes:
            note_node_id = id_mapping.get(("note", note.id))
            if not note_node_id:
                continue

            for related in note.related_notes.all():
                related_node_id = id_mapping.get(("note", related.id))
                if related_node_id:
                    # 避免重复链接
                    link_id = f"note-{note.id}-related-{related.id}"
                    if not any(getattr(lnk, "id", None) == link_id for lnk in links):
                        link = type("Link", (), {
                            "id": link_id,
                            "source_id": note_node_id,
                            "target_id": related_node_id,
                            "link_type": "related",
                        })()
                        links.append(link)

    # 6. 获取手动创建的链接
    if mode in ("hybrid", "manual_only"):
        manual_links = GraphLink.objects.filter(owner=user)
        for link in manual_links:
            links.append(link)

    return {
        "nodes": [_serialize_node(node) for node in nodes],
        "links": [_serialize_link(link) for link in links],
    }


def get_related_graph_data(
    user: object, node_id: int
) -> dict[str, list[dict[str, object]]]:
    """
    获取指定节点相关的节点与链接

    支持两种类型的节点：
    - 手动创建的节点（GraphNode，整数 ID）
    - 同步节点（笔记/分类/标签，字符串格式 ID 如 "note-123"）

    Returns:
        {"nodes": [...], "links": [...]} 的字典
    """
    nodes = []
    links = []

    # 判断是手动节点还是同步节点
    # 同步节点的 ID 是字符串格式，如 "note-123"
    if isinstance(node_id, str) and node_id.startswith(("note-", "category-", "tag-")):
        # 同步节点：从完整图谱数据中筛选
        hybrid_data = get_hybrid_graph_data(user, "hybrid")

        # 找到点击的节点及其相关的节点和链接
        related_node_ids = set()

        # 找到所有相关的链接
        for link in hybrid_data.get("links", []):
            source = link.get("source")
            target = link.get("target")
            if source == node_id:
                related_node_ids.add(target)
            if target == node_id:
                related_node_ids.add(source)

        # 收集相关节点（包括被点击的节点和与其相连的节点）
        for node in hybrid_data.get("nodes", []):
            if node.get("id") == node_id or node.get("id") in related_node_ids:
                nodes.append(node)

        # 收集相关链接
        for link in hybrid_data.get("links", []):
            source = link.get("source")
            target = link.get("target")
            if source == node_id or target == node_id:
                links.append(type("Link", (), {
                    "id": link.get("id"),
                    "source_id": source,
                    "target_id": target,
                    "link_type": link.get("type", "related"),
                })())

    else:
        # 手动节点：从 GraphNode 表查询
        # 尝试将 node_id 转换为整数
        try:
            numeric_node_id = int(node_id)
        except (ValueError, TypeError):
            numeric_node_id = None

        if numeric_node_id is not None:
            links = GraphLink.objects.filter(owner=user).filter(
                Q(source_id=numeric_node_id) | Q(target_id=numeric_node_id)
            )

            node_ids = {numeric_node_id}
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
