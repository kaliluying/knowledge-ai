"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Apply WSGI middleware for static files in production
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# Optional: Add WhiteNoise for static files in production
# from whitenoise import WhiteNoise
# application = WhiteNoise(application, root=PROJECT_ROOT / 'staticfiles')

# Configure logging
from utils.logging import setup_logging

log_level = os.getenv("DJANGO_LOG_LEVEL", "INFO")
setup_logging(log_level=log_level)
