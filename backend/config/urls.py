"""
URL configuration for config project.

API Structure:
- /api/auth/ - Authentication endpoints
- /api/notes/ - Notes management
- /api/categories/ - Categories management
- /api/tags/ - Tags management
- /api/graph/ - Knowledge graph
- /api/collections/ - Content collections
- /api/attachments/ - File attachments
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # API Authentication
    path("api/auth/", include("apps.users.urls")),
    # API Notes
    path("api/notes/", include("apps.notes.urls")),
    # API Categories
    path("api/categories/", include("apps.categories.urls")),
    # API Tags
    path("api/tags/", include("apps.tags.urls")),
    # API Knowledge Graph
    path("api/graph/", include("apps.graph.urls")),
    # API Collections
    path("api/collections/", include("apps.collections.urls")),
    # API Attachments
    path("api/attachments/", include("apps.attachments.urls")),
    # Health check
    path("api/health/", lambda request: {"status": "ok"}, name="health"),
]

# Media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
