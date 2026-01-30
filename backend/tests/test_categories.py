"""
Tests for the category management module.
"""

import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestCategoryCRUD:
    """Tests for category CRUD operations."""

    def test_create_category(self, authenticated_client):
        """Test creating a new category."""
        data = {"name": "New Category", "slug": "new-category", "color": "#2ecc71"}
        response = authenticated_client.post("/api/categories/", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["code"] == 200
        assert response.data["data"]["name"] == "New Category"

    def test_list_categories(self, authenticated_client, test_category):
        """Test listing all categories."""
        response = authenticated_client.get("/api/categories/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["code"] == 200
        assert len(response.data["data"]) >= 1

    def test_get_category_detail(self, authenticated_client, test_category):
        """Test getting category detail."""
        response = authenticated_client.get(f"/api/categories/{test_category.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["name"] == test_category.name

    def test_update_category(self, authenticated_client, test_category):
        """Test updating a category."""
        data = {"name": "Updated Category", "color": "#9b59b6"}
        response = authenticated_client.put(
            f"/api/categories/{test_category.id}/", data, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        test_category.refresh_from_db()
        assert test_category.name == "Updated Category"

    def test_delete_category(self, authenticated_client, test_category):
        """Test deleting a category."""
        response = authenticated_client.delete(f"/api/categories/{test_category.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_create_category_unauthenticated(self, api_client):
        """Test that unauthenticated users cannot create categories."""
        data = {"name": "New Category", "slug": "new-category", "color": "#2ecc71"}
        response = api_client.post("/api/categories/", data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestCategoryTree:
    """Tests for category tree functionality."""

    def test_get_category_tree(self, authenticated_client):
        """Test getting category tree structure."""
        response = authenticated_client.get("/api/categories/tree/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["code"] == 200
