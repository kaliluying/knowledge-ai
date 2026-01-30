"""
Tests for graph services.
"""

import pytest

from apps.graph.models import GraphNode, GraphLink
from apps.graph.services import get_graph_data, get_related_graph_data


pytestmark = pytest.mark.django_db


def test_get_graph_data_returns_nodes_and_links(test_user):
    node_one = GraphNode.objects.create(
        owner=test_user,
        node_type="note",
        title="First Note",
        data={"value": 3, "category": "Tech", "tags": ["python", "django"]},
    )
    node_two = GraphNode.objects.create(
        owner=test_user,
        node_type="tag",
        title="Django",
    )
    link = GraphLink.objects.create(
        owner=test_user,
        source=node_one,
        target=node_two,
        link_type="related",
    )

    payload = get_graph_data(test_user)

    assert len(payload["nodes"]) == 2
    assert len(payload["links"]) == 1

    node_payload = next(item for item in payload["nodes"] if item["id"] == node_one.id)
    assert node_payload["name"] == node_one.label
    assert node_payload["type"] == "note"
    assert node_payload["value"] == 3
    assert node_payload["category"] == "Tech"
    assert node_payload["tags"] == ["python", "django"]
    assert "created_at" in node_payload

    link_payload = payload["links"][0]
    assert link_payload["id"] == link.id
    assert link_payload["source"] == node_one.id
    assert link_payload["target"] == node_two.id
    assert link_payload["type"] == "related"
    assert link_payload["strength"] == 1


def test_get_related_graph_data_filters_nodes(test_user):
    node_one = GraphNode.objects.create(
        owner=test_user,
        node_type="note",
        title="Root Note",
    )
    node_two = GraphNode.objects.create(
        owner=test_user,
        node_type="tag",
        title="Tag",
    )
    node_three = GraphNode.objects.create(
        owner=test_user,
        node_type="category",
        title="Category",
    )

    GraphLink.objects.create(
        owner=test_user,
        source=node_one,
        target=node_two,
        link_type="related",
    )
    GraphLink.objects.create(
        owner=test_user,
        source=node_two,
        target=node_three,
        link_type="related",
    )

    payload = get_related_graph_data(test_user, node_one.id)

    node_ids = {node["id"] for node in payload["nodes"]}
    link_ids = {link["source"] for link in payload["links"]}
    link_targets = {link["target"] for link in payload["links"]}

    assert node_one.id in node_ids
    assert node_two.id in node_ids
    assert node_three.id not in node_ids
    assert node_one.id in link_ids
    assert node_two.id in link_targets
