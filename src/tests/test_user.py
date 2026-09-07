import pytest
from src.roles import UserRole
from src.api.core.settings import settings

def test_admin_create(create_admin):
    assert create_admin.role == UserRole.ADMIN
    assert create_admin.email == settings.admin_email

def test_admin_login(login_admin):
    assert "access_token" in login_admin
    assert "refresh_token" in login_admin
    assert login_admin["token_type"] == "bearer"

def test_admin_auth(auth_admin):
    assert "Authorization" in auth_admin