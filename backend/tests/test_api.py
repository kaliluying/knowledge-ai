"""
Integration tests for API endpoints.
"""

import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestAPIIntegration:
    """Integration tests for main API endpoints."""

    def test_full_user_flow(self, api_client):
        """Test complete user registration and authentication flow."""
        # Register user
        register_data = {
            "username": "flowuser",
            "email": "flow@example.com",
            "password": "flowpass123",
            "password_confirm": "flowpass123",
        }
        response = api_client.post("/api/auth/register/", register_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        user_id = response.data["data"]["id"]

        # Login
        login_data = {"username": "flowuser", "password": "flowpass123"}
        response = api_client.post("/api/auth/login/", login_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        token = response.data["access"]

        # Access profile with token
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = api_client.get("/api/auth/profile/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["username"] == "flowuser"

    def test_crud_flow_with_relations(
        self, authenticated_client, test_user, test_category, test_tag
    ):
        """Test CRUD flow with related objects."""
        # Create note with category and tags
        note_data = {
            "title": "Integration Test Note",
            "content": "<p>Testing integration.</p>",
            "category": test_category.id,
            "tags": [test_tag.id],
        }
        response = authenticated_client.post("/api/notes/", note_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        note_id = response.data["data"]["id"]

        # Retrieve note
        response = authenticated_client.get(f"/api/notes/{note_id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["title"] == "Integration Test Note"

        # Update note
        update_data = {
            "title": "Updated Integration Test",
            "content": "<p>Updated content.</p>",
        }
        response = authenticated_client.put(
            f"/api/notes/{note_id}/", update_data, format="json"
        )
        assert response.status_code == status.HTTP_200_OK

        # Delete note
        response = authenticated_client.delete(f"/api/notes/{note_id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify deletion
        response = authenticated_client.get(f"/api/notes/{note_id}/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_endpoints_require_authentication(self, api_client):
        """Test that protected endpoints require authentication."""
        protected_endpoints = [
            ("/api/categories/", "post"),
            ("/api/tags/", "post"),
            ("/api/notes/", "post"),
            ("/api/auth/profile/", "get"),
        ]

        for endpoint, method in protected_endpoints:
            if method == "get":
                response = api_client.get(endpoint)
            elif method == "post":
                response = api_client.post(endpoint, {}, format="json")

            assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
                f"Endpoint {method.upper()} {endpoint} should require authentication"
            )

    def test_api_response_format(self, authenticated_client):
        """Test that API responses follow the consistent format."""
        response = authenticated_client.get("/api/categories/")
        assert response.status_code == status.HTTP_200_OK
        assert "code" in response.data
        assert "message" in response.data
        assert "data" in response.data
