"""
Notes signals.

Keep GraphNode in sync with Note lifecycle.
Create GraphLinks between notes and categories/tags.
Detect internal references in note content.
"""

import re
from django.db import models
from django.db.models.signals import m2m_changed, post_delete, post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from apps.graph.models import GraphNode, GraphLink
from .models import Note


def _generate_unique_slug(title: str, current_note_id: int | None = None) -> str:
    base_slug = slugify(title) or "note"
    slug = base_slug
    suffix = 1

    queryset = Note.objects.filter(slug=slug)
    if current_note_id is not None:
        queryset = queryset.exclude(id=current_note_id)

    while queryset.exists():
        slug = f"{base_slug}-{suffix}"
        suffix += 1
        queryset = Note.objects.filter(slug=slug)
        if current_note_id is not None:
            queryset = queryset.exclude(id=current_note_id)

    return slug


@receiver(pre_save, sender=Note)
def ensure_note_slug(sender, instance, **kwargs):
    """保存前确保 slug 已生成且唯一。"""
    if not instance.title:
        return

    if not instance.slug:
        instance.slug = _generate_unique_slug(instance.title, instance.id)


def _build_note_data(note: object) -> dict[str, object]:
    category = getattr(note, "category", None)
    category_name = category.name if category else None
    tags_manager = getattr(note, "tags", None)
    tag_names = (
        list(tags_manager.values_list("name", flat=True))
        if tags_manager is not None
        else []
    )
    return {
        "note_id": getattr(note, "id", None),
        "category": category_name,
        "tags": tag_names,
        "is_pinned": getattr(note, "is_pinned", False),
        "is_archived": getattr(note, "is_archived", False),
    }


def _extract_referenced_note_ids(plain_text: str) -> list[int]:
    """从纯文本中提取引用的笔记 ID。

    支持格式：
    - [[note:123]]
    - [[123]]
    """
    ids = set()
    # Match [[note:123]] or [[123]]
    pattern = r"\[\[(?:note:)?(\d+)\]\]"
    for match in re.finditer(pattern, plain_text):
        try:
            ids.add(int(match.group(1)))
        except ValueError:
            pass
    return list(ids)


@receiver(post_save, sender=Note)
def sync_note_node(sender, instance, created, **kwargs):
    """Create or update GraphNode when note is saved."""
    data = _build_note_data(instance)

    node = GraphNode.objects.filter(
        owner=instance.owner,
        node_type="note",
        data__note_id=instance.id,
    ).first()

    if node:
        node.title = instance.title
        node.label = instance.title
        node.data = data
        node.save(update_fields=["title", "label", "data", "updated_at"])
    else:
        GraphNode.objects.create(
            owner=instance.owner,
            node_type="note",
            title=instance.title,
            label=instance.title,
            data=data,
        )

    # Update links to category and tags
    _sync_note_category_link(instance)
    _sync_note_tags_links(instance)
    _sync_note_reference_links(instance)


@receiver(post_delete, sender=Note)
def remove_note_node(sender, instance, **kwargs):
    """Remove GraphNode when note is deleted."""
    # First get the GraphNode IDs to clean up links
    note_node_ids = list(
        GraphNode.objects.filter(
            owner=instance.owner,
            node_type="note",
            data__note_id=instance.id,
        ).values_list("id", flat=True)
    )

    # Delete the GraphNode
    GraphNode.objects.filter(
        owner=instance.owner,
        node_type="note",
        data__note_id=instance.id,
    ).delete()

    # Clean up reference links using the node IDs we captured
    if note_node_ids:
        GraphLink.objects.filter(
            owner=instance.owner,
            link_type="reference",
        ).filter(
            models.Q(source_id__in=note_node_ids)
            | models.Q(target_id__in=note_node_ids)
        ).delete()

    # Also clean up category and tag links for this note
    GraphLink.objects.filter(
        owner=instance.owner,
    ).filter(
        models.Q(source_id__in=note_node_ids) | models.Q(target_id__in=note_node_ids)
    ).delete()


def _sync_note_category_link(note: Note):
    """Create or update link between note and its category."""
    if not note.category_id:
        return

    # Get the GraphNode for the note
    note_node = GraphNode.objects.filter(
        owner=note.owner,
        node_type="note",
        data__note_id=note.id,
    ).first()

    # Get the GraphNode for the category
    category_node = GraphNode.objects.filter(
        owner=note.owner,
        node_type="category",
        data__category_id=note.category_id,
    ).first()

    if not note_node or not category_node:
        return

    # Create or update the link
    GraphLink.objects.update_or_create(
        owner=note.owner,
        source=note_node,
        target=category_node,
        defaults={
            "link_type": "parent",
        },
    )


def _sync_note_tags_links(note: Note):
    """Create or update links between note and its tags."""
    note_node = GraphNode.objects.filter(
        owner=note.owner,
        node_type="note",
        data__note_id=note.id,
    ).first()

    if not note_node:
        return

    # Get tag IDs
    tag_ids = list(note.tags.values_list("id", flat=True))

    # Get existing tag links
    existing_links = list(
        GraphLink.objects.filter(
            owner=note.owner,
            source=note_node,
            link_type="tagged",
        )
    )

    # Get existing target IDs (GraphNode IDs for tags)
    existing_target_ids = {link.target_id for link in existing_links}

    # Find new tag node IDs by querying each tag
    new_target_ids = set()
    for tag_id in tag_ids:
        node = GraphNode.objects.filter(
            owner=note.owner,
            node_type="tag",
            data__tag_id=str(tag_id),
        ).first()
        if node:
            new_target_ids.add(node.id)

    # Remove links for tags that are no longer attached
    for link in existing_links:
        if link.target_id not in new_target_ids:
            link.delete()

    # Create links for new tags
    for node_id in new_target_ids:
        if node_id not in existing_target_ids:
            target_node = GraphNode.objects.get(id=node_id)
            GraphLink.objects.create(
                owner=note.owner,
                source=note_node,
                target=target_node,
                link_type="tagged",
            )


def _sync_note_reference_links(note: Note):
    """Create links to other notes referenced in content."""
    note_node = GraphNode.objects.filter(
        owner=note.owner,
        node_type="note",
        data__note_id=note.id,
    ).first()

    if not note_node:
        return

    # Extract referenced note IDs from plain text
    referenced_ids = _extract_referenced_note_ids(note.plain_text)

    if not referenced_ids:
        # Remove existing reference links if no references
        GraphLink.objects.filter(
            owner=note.owner,
            source=note_node,
            link_type="reference",
        ).delete()
        return

    # Get referenced note nodes - query each note separately to avoid JSONB type issues
    referenced_nodes = []
    for ref_id in referenced_ids:
        node = GraphNode.objects.filter(
            owner=note.owner,
            node_type="note",
            data__note_id=str(ref_id),
        ).first()
        if node:
            referenced_nodes.append(node)

    # Get existing reference links
    existing_links = list(
        GraphLink.objects.filter(
            owner=note.owner,
            source=note_node,
            link_type="reference",
        )
    )

    # Remove links for notes that are no longer referenced
    existing_target_ids = {link.target_id for link in existing_links}
    new_target_ids = {node.id for node in referenced_nodes}

    for link in existing_links:
        if link.target_id not in new_target_ids:
            link.delete()

    # Create links for new references
    for ref_node in referenced_nodes:
        if ref_node.id not in existing_target_ids:
            GraphLink.objects.create(
                owner=note.owner,
                source=note_node,
                target=ref_node,
                link_type="reference",
            )


@receiver(m2m_changed, sender=Note.tags.through)
def note_tags_changed(sender, instance, action, **kwargs):
    """Handle many-to-many changes on note tags."""
    if action in ("post_add", "post_remove", "post_clear"):
        _sync_note_tags_links(instance)
