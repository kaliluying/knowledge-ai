"""
Tests for the note management module.
"""

import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestNoteCRUD:
    """Tests for note CRUD operations."""

    def test_create_note(self, authenticated_client, test_category):
        """Test creating a new note."""
        data = {
            "title": "New Note",
            "content": "<p>This is a new note.</p>",
            "category": test_category.id,
        }
        response = authenticated_client.post("/api/notes/", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["code"] == 200
        assert response.data["data"]["title"] == "New Note"

    def test_list_notes(self, authenticated_client, test_note):
        """Test listing all notes."""
        response = authenticated_client.get("/api/notes/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["code"] == 200
        assert len(response.data["data"]) >= 1

    def test_get_note_detail(self, authenticated_client, test_note):
        """Test getting note detail."""
        response = authenticated_client.get(f"/api/notes/{test_note.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["title"] == test_note.title

    def test_update_note(self, authenticated_client, test_note):
        """Test updating a note."""
        data = {"title": "Updated Note", "content": "<p>Updated content.</p>"}
        response = authenticated_client.put(
            f"/api/notes/{test_note.id}/", data, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        test_note.refresh_from_db()
        assert test_note.title == "Updated Note"

    def test_delete_note(self, authenticated_client, test_note):
        """Test deleting a note."""
        response = authenticated_client.delete(f"/api/notes/{test_note.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_create_note_unauthenticated(self, api_client, test_category):
        """Test that unauthenticated users cannot create notes."""
        data = {
            "title": "New Note",
            "content": "<p>This is a new note.</p>",
            "category": test_category.id,
        }
        response = api_client.post("/api/notes/", data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestNoteSearch:
    """Tests for note search functionality."""

    def test_search_notes(self, authenticated_client, test_note):
        """Test searching notes."""
        response = authenticated_client.get("/api/notes/search/?q=Test")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["code"] == 200

    def test_recent_notes(self, authenticated_client, test_note):
        """Test getting recent notes."""
        response = authenticated_client.get("/api/notes/recent/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["code"] == 200


class TestNoteArchive:
    """Tests for note archive functionality."""

    def test_archive_note(self, authenticated_client, test_note):
        """Test archiving a note."""
        response = authenticated_client.post(
            f"/api/notes/{test_note.id}/archive/", format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        test_note.refresh_from_db()
        assert test_note.is_archived is True
