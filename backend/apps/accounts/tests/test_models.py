"""Model-level tests for the custom User foundation (issue #1)."""

import pytest
from django.db import IntegrityError

from apps.accounts.models import User

pytestmark = pytest.mark.django_db


class TestUserManager:
    def test_create_user_normalizes_email_domain(self):
        user = User.objects.create_user(email="juan@EXAMPLE.COM", password="secret-pass-123")
        assert user.email == "juan@example.com"
        assert user.is_active is True
        assert user.is_staff is False
        assert user.check_password("secret-pass-123")

    def test_create_user_without_email_is_rejected(self):
        with pytest.raises(ValueError):
            User.objects.create_user(email="", password="secret-pass-123")

    def test_emails_are_unique(self):
        User.objects.create_user(email="dup@test.dev", password="secret-pass-123")
        with pytest.raises(IntegrityError):
            User.objects.create_user(email="dup@test.dev", password="other-pass-456")

    def test_create_superuser_sets_flags(self):
        user = User.objects.create_superuser(email="admin@test.dev", password="secret-pass-123")
        assert user.is_staff is True
        assert user.is_superuser is True

    def test_superuser_requires_staff_flag(self):
        with pytest.raises(ValueError, match="is_staff"):
            User.objects.create_superuser(
                email="broken@test.dev",
                password="secret-pass-123",
                is_staff=False,
            )
