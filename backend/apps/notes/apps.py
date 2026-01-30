"""
Notes app configuration.
"""

from django.apps import AppConfig


class NotesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.notes"
    verbose_name = "笔记"

    def ready(self) -> None:
        from . import signals  # noqa: F401
