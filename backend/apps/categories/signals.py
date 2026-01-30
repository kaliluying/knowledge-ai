"""
Categories signals.

Keep GraphNode in sync with Category lifecycle.
"""

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.graph.models import GraphNode
from .models import Category


def _build_category_data(category: object) -> dict[str, object]:
    return {
        "path": getattr(category, "path", None),
        "color": getattr(category, "color", None),
    }


@receiver(post_save, sender=Category)
def sync_category_node(sender, instance, created, **kwargs):
    """Create or update GraphNode when category is saved."""
    data = _build_category_data(instance)

    # Find existing node by looking for node with same owner and matching data
    node = GraphNode.objects.filter(
        owner=instance.owner,
        node_type="category",
        data__category_id=getattr(instance, "id", None),
    ).first()

    if node:
        node.title = getattr(instance, "name", "")
        node.label = getattr(instance, "name", "")
        node.data = data
        node.save(update_fields=["title", "label", "data", "updated_at"])
    else:
        GraphNode.objects.create(
            owner=instance.owner,
            node_type="category",
            title=getattr(instance, "name", ""),
            label=getattr(instance, "name", ""),
            data={
                **data,
                "category_id": getattr(instance, "id", None),
            },
        )


@receiver(post_delete, sender=Category)
def remove_category_node(sender, instance, **kwargs):
    """Remove GraphNode when category is deleted."""
    GraphNode.objects.filter(
        owner=instance.owner,
        node_type="category",
        data__category_id=getattr(instance, "id", None),
    ).delete()
