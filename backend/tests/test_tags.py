"""
Tests for the tag management module.
"""

import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestTagCRUD:
    """Tests for tag CRUD operations."""

    def test_create_tag(self, authenticated_client):
        """Test creating a new tag."""
        data = {"name": "New Tag", "slug": "new-tag", "color": "#e74c3c"}
        response = authenticated_client.post("/api/tags/", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["code"] == 200
        assert response.data["data"]["name"] == "New Tag"

    def test_list_tags(self, authenticated_client, test_tag):
        """Test listing all tags."""
        response = authenticated_client.get("/api/tags/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["code"] == 200
        assert len(response.data["data"]) >= 1

    def test_get_tag_detail(self, authenticated_client, test_tag):
        """Test getting tag detail."""
        response = authenticated_client.get(f"/api/tags/{test_tag.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["name"] == test_tag.name

    def test_update_tag(self, authenticated_client, test_tag):
        """Test updating a tag."""
        data = {"name": "Updated Tag", "color": "#3498db"}
        response = authenticated_client.put(
            f"/api/tags/{test_tag.id}/", data, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        test_tag.refresh_from_db()
        assert test_tag.name == "Updated Tag"

    def test_delete_tag(self, authenticated_client, test_tag):
        """Test deleting a tag."""
        response = authenticated_client.delete(f"/api/tags/{test_tag.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_create_tag_unauthenticated(self, api_client):
        """Test that unauthenticated users cannot create tags."""
        data = {"name": "New Tag", "slug": "new-tag", "color": "#e74c3c"}
        response = api_client.post("/api/tags/", data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestTagList:
    """Tests for tag list functionality."""

    def test_get_tag_list_minimal(self, authenticated_client, test_tag):
        """Test getting tag list with minimal fields."""
        response = authenticated_client.get("/api/tags/?minimal=true")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["code"] == 200
