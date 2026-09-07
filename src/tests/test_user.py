import pytest
from src.roles import UserRole
from src.api.core.settings import settings

def test_admin_create(create_admin):
    assert create_admin.role == UserRole.ADMIN
    assert create_admin.email == settings.admin_email