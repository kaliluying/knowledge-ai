"""
Logging configuration module

Django logging setup with console and file handlers
"""

import os
import logging
import logging.handlers
from datetime import datetime

# Log directory
LOG_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs"
)

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)


def setup_logging(log_level: str = "INFO", log_file: str = "django.log") -> None:
    """
    Setup Django logging configuration

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Log filename
    """
    # Clear existing handlers
    logging.root.handlers = []

    # Get logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler with rotation
    log_path = os.path.join(LOG_DIR, log_file)
    file_handler = logging.handlers.TimedRotatingFileHandler(
        log_path, when="midnight", interval=1, backupCount=14, encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Django-specific loggers
    # Database queries
    logging.getLogger("django.db.backends").setLevel(logging.INFO)

    # Django security warnings
    logging.getLogger("django.security").setLevel(logging.WARNING)

    # Request/response logging
    logging.getLogger("django.request").setLevel(logging.INFO)

    # Third-party packages
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the given name

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)
