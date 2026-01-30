"""
Pytest configuration and fixtures for backend tests.
"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def test_user(db):
    """Create a test user."""
    user = User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    return user


@pytest.fixture
def test_category(db, test_user):
    """Create a test category."""
    from apps.categories.models import Category

    category = Category.objects.create(
        name="Test Category", slug="test-category", color="#3498db", owner=test_user
    )
    return category


@pytest.fixture
def test_tag(db, test_user):
    """Create a test tag."""
    from apps.tags.models import Tag

    tag = Tag.objects.create(
        name="Test Tag", slug="test-tag", color="#e74c3c", owner=test_user
    )
    return tag


@pytest.fixture
def test_note(db, test_user, test_category, test_tag):
    """Create a test note."""
    from apps.notes.models import Note

    note = Note.objects.create(
        title="Test Note",
        content=[
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": "This is a test note content."}],
            }
        ],
        plain_text="This is a test note content.",
        owner=test_user,
        category=test_category,
    )
    note.tags.add(test_tag)
    return note


@pytest.fixture
def api_client():
    """Create an unauthenticated API client."""
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, test_user):
    """Create an authenticated API client."""
    from rest_framework_simplejwt.tokens import RefreshToken

    refresh = RefreshToken.for_user(test_user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client
