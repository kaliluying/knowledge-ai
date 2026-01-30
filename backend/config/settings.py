import os
import logging
import logging.handlers
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


# Quick-start development settings - unsuitable for production
SECRET_KEY = get_required_env("SECRET_KEY")

# Security: DEBUG should be False in production
# 设置为 False 以防止生产环境信息泄露
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Logging configuration
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)


def get_logging_config():
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "simple": {
                "format": "%(asctime)s [%(levelname)s] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "filters": {
            "require_debug_true": {
                "()": "django.utils.log.RequireDebugTrue",
            },
            "require_debug_false": {
                "()": "django.utils.log.RequireDebugFalse",
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "filters": ["require_debug_true"],
                "class": "logging.StreamHandler",
                "formatter": "simple",
            },
            "file": {
                "level": "INFO",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": str(LOG_DIR / "django.log"),
                "when": "midnight",
                "backupCount": 14,
                "encoding": "utf-8",
                "formatter": "verbose",
            },
            "error_file": {
                "level": "ERROR",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": str(LOG_DIR / "errors.log"),
                "when": "midnight",
                "backupCount": 30,
                "encoding": "utf-8",
                "formatter": "verbose",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": True,
            },
            "django.db.backends": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": False,
            },
            "django.security": {
                "handlers": ["console", "error_file"],
                "level": "WARNING",
                "propagate": False,
            },
            "django.request": {
                "handlers": ["console", "file", "error_file"],
                "level": "INFO",
                "propagate": False,
            },
            "apps": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": False,
            },
            "urllib3": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False,
            },
        },
    }


LOGGING = get_logging_config()

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party apps
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "django_filters",
    "mptt",
    # Local apps
    "apps.users",
    "apps.notes.apps.NotesConfig",
    "apps.categories",
    "apps.tags",
    "apps.graph",
    "apps.collections",
    "apps.attachments",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "utils.middleware.RateLimitMiddleware",  # 速率限制中间件
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database - PostgreSQL Configuration
# 从环境变量读取配置
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DATABASE_NAME", "knowledge_db"),
        "USER": os.getenv("DATABASE_USER", "postgres"),
        "PASSWORD": get_required_env("DATABASE_PASSWORD"),
        "HOST": os.getenv("DATABASE_HOST", "localhost"),
        "PORT": os.getenv("DATABASE_PORT", "5432"),
        # 数据库连接池配置：生产环境建议启用
        # CONN_MAX_AGE 设置连接保持时间（秒），0 表示每次请求新建连接
        # 设置为 600（10分钟）可以减少连接建立开销，提高性能
        "CONN_MAX_AGE": int(os.getenv("DATABASE_CONN_MAX_AGE", "0")),
    }
}

# Custom user model
AUTH_USER_MODEL = "users.User"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    {
        "NAME": "utils.password_validators.StrongPasswordValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
]

# Cache configuration (for rate limiting)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

# Internationalization
LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# REST Framework Configuration
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "utils.pagination.StandardPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "EXCEPTION_HANDLER": "utils.exceptions.custom_exception_handler",
}

# JWT Configuration
# 使用独立的 JWT 签名密钥，防止与 SECRET_KEY 混淆
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_LIFETIME = timedelta(minutes=15)  # 访问令牌 15 分钟
REFRESH_TOKEN_LIFETIME = timedelta(days=1)  # 刷新令牌 1 天

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": ACCESS_TOKEN_LIFETIME,
    "REFRESH_TOKEN_LIFETIME": REFRESH_TOKEN_LIFETIME,
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": JWT_ALGORITHM,
    "SIGNING_KEY": JWT_SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://knowledge.yourdomain.com",  # 生产环境
    "https://www.knowledge.yourdomain.com",
]

CORS_ALLOW_CREDENTIALS = True

# CSRF Configuration (required for production)
CSRF_TRUSTED_ORIGINS = [
    "https://knowledge.yourdomain.com",
    "https://www.knowledge.yourdomain.com",
]

# Security Headers Configuration
# These settings help protect against common web attacks

# X-Frame-Options: Prevent clickjacking attacks by controlling iframe embedding
X_FRAME_OPTIONS = "DENY"

# X-Content-Type-Options: Prevent MIME type sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True

# X-XSS-Protection: Enable browser's XSS filtering (legacy, but still useful)
SECURE_BROWSER_XSS_FILTER = True

# Strict-Transport-Security (HSTS): Enforce HTTPS connections
# Uncomment in production after verifying SSL certificate works
# SECURE_HSTS_SECONDS = 31536000  # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# Referrer-Policy: Control referrer information sent to other sites
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# Permissions-Policy: Control browser features and APIs
SECURE_PERMISSIONS_POLICY = "geolocation=(), microphone=(), camera=()"
