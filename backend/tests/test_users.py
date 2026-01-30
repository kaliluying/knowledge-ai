"""
Tests for the user authentication module.
"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestUserRegistration:
    """Tests for user registration functionality."""

    def test_register_user_success(self, api_client):
        """Test successful user registration."""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepass123",
            "password_confirm": "securepass123",
        }
        response = api_client.post("/api/auth/register/", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["code"] == 201
        assert User.objects.filter(username="newuser").exists()

    def test_register_duplicate_username(self, api_client, test_user):
        """Test registration with duplicate username."""
        data = {
            "username": "testuser",
            "email": "another@example.com",
            "password": "securepass123",
            "password_confirm": "securepass123",
        }
        response = api_client.post("/api/auth/register/", data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_password_mismatch(self, api_client):
        """Test registration with mismatched passwords."""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepass123",
            "password_confirm": "differentpass",
        }
        response = api_client.post("/api/auth/register/", data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserLogin:
    """Tests for user login functionality."""

    def test_login_success(self, api_client, test_user):
        """Test successful user login."""
        data = {"email": "test@example.com", "password": "testpass123"}
        response = api_client.post("/api/auth/login/", data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data["data"]
        assert "refresh" in response.data["data"]

    def test_login_invalid_credentials(self, api_client, test_user):
        """Test login with invalid credentials."""
        data = {"email": "test@example.com", "password": "wrongpassword"}
        response = api_client.post("/api/auth/login/", data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_nonexistent_user(self, api_client):
        """Test login with nonexistent user."""
        data = {"email": "nonexistent@example.com", "password": "somepassword"}
        response = api_client.post("/api/auth/login/", data, format="json")
        # The serializer validates first, so we get 400 for invalid user before 401
        assert response.status_code in [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_401_UNAUTHORIZED,
        ]


@pytest.mark.django_db
class TestUserProfile:
    """Tests for user profile functionality."""

    def test_get_profile_authenticated(self, authenticated_client, test_user):
        """Test getting profile for authenticated user."""
        response = authenticated_client.get("/api/auth/profile/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["username"] == "testuser"

    def test_get_profile_unauthenticated(self, api_client):
        """Test that unauthenticated users cannot get profile."""
        response = api_client.get("/api/auth/profile/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_profile(self, authenticated_client, test_user):
        """Test updating user profile."""
        data = {"bio": "Updated bio", "avatar": "https://example.com/avatar.jpg"}
        response = authenticated_client.put("/api/auth/profile/", data, format="json")
        assert response.status_code == status.HTTP_200_OK
        test_user.refresh_from_db()
        assert test_user.bio == "Updated bio"
