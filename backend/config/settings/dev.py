"""Development settings.

Database is selected by environment:
- If POSTGRES_HOST is set (e.g. inside Docker Compose), PostgreSQL is used.
- Otherwise falls back to local SQLite so the project runs bare-metal with zero setup.
"""

import os

from config.settings.base import *  # noqa: F403

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY", "django-insecure-dev-only-do-not-use-in-production"
)

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

if os.environ.get("POSTGRES_HOST"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "nexus"),
            "USER": os.environ.get("POSTGRES_USER", "nexus"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
            "HOST": os.environ["POSTGRES_HOST"],
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
        }
    }
