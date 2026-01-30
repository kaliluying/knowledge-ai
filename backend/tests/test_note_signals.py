"""
Tests for note signals syncing GraphNode.
"""

import pytest

from apps.graph.models import GraphNode
from apps.notes.models import Note


pytestmark = pytest.mark.django_db


def test_note_create_creates_graph_node(test_user, test_category, test_tag):
    note = Note.objects.create(
        title="Signal Note",
        content=[{"type": "paragraph", "content": [{"type": "text", "text": "hi"}]}],
        owner=test_user,
        category=test_category,
    )
    note.tags.add(test_tag)
    note.save()

    node = GraphNode.objects.filter(
        owner=test_user,
        node_type="note",
        data__note_id=note.id,
    ).first()

    assert node is not None
    assert node.title == "Signal Note"
    assert node.data["category"] == test_category.name
    assert test_tag.name in node.data["tags"]


def test_note_update_updates_graph_node(test_user):
    note = Note.objects.create(
        title="Original",
        content=[{"type": "paragraph", "content": [{"type": "text", "text": "hi"}]}],
        owner=test_user,
    )

    note.title = "Updated"
    note.save()

    node = GraphNode.objects.get(
        owner=test_user,
        node_type="note",
        data__note_id=note.id,
    )
    assert node.title == "Updated"
    assert node.label == "Updated"


def test_note_delete_removes_graph_node(test_user):
    note = Note.objects.create(
        title="To Remove",
        content=[{"type": "paragraph", "content": [{"type": "text", "text": "hi"}]}],
        owner=test_user,
    )
    node_id = GraphNode.objects.get(
        owner=test_user,
        node_type="note",
        data__note_id=note.id,
    ).id

    note.delete()

    assert not GraphNode.objects.filter(id=node_id).exists()
