"""
Tags signals.

Keep GraphNode in sync with Tag lifecycle.
"""

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.graph.models import GraphNode
from .models import Tag


def _build_tag_data(tag: object) -> dict[str, object]:
    return {
        "color": getattr(tag, "color", None),
        "usage_count": getattr(tag, "usage_count", 0),
    }


@receiver(post_save, sender=Tag)
def sync_tag_node(sender, instance, created, **kwargs):
    """Create or update GraphNode when tag is saved."""
    data = _build_tag_data(instance)

    node = GraphNode.objects.filter(
        owner=instance.owner,
        node_type="tag",
        data__tag_id=getattr(instance, "id", None),
    ).first()

    if node:
        node.title = getattr(instance, "name", "")
        node.label = getattr(instance, "name", "")
        node.data = data
        node.save(update_fields=["title", "label", "data", "updated_at"])
    else:
        GraphNode.objects.create(
            owner=instance.owner,
            node_type="tag",
            title=getattr(instance, "name", ""),
            label=getattr(instance, "name", ""),
            data={
                **data,
                "tag_id": getattr(instance, "id", None),
            },
        )


@receiver(post_delete, sender=Tag)
def remove_tag_node(sender, instance, **kwargs):
    """Remove GraphNode when tag is deleted."""
    GraphNode.objects.filter(
        owner=instance.owner,
        node_type="tag",
        data__tag_id=getattr(instance, "id", None),
    ).delete()
