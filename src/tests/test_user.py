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

def test_refresh_token(client, user_login):
    refresh_token = user_login["refresh_token"]

    res = client.post("/auth/refresh", json={"refresh_token": refresh_token})

    assert res.status_code == 200

    data = res.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_old_refresh_token(client, user_login):
    refresh_token = user_login["refresh_token"]
    
    res = client.post("/auth/refresh", json={"refresh_token": refresh_token})

    assert res.status_code == 200

    data = res.json()

    assert data["refresh_token"] != refresh_token

    res = client.post("/auth/refresh", json={"refresh_token": refresh_token})

    assert res.status_code == 401

def test_random_refresh_token(client):
    res = client.post("/auth/refresh", json={"refresh_token": "randon_token"})

    assert res.status_code == 401
    assert "refresh_token" not in res.json()

def test_access_token_instead_od_refresh(client, user_login):
    access_token = user_login['access_token']

    res = client.post("/auth/refresh", json={"refresh_token": access_token})
    
    assert res.status_code == 401

def test_no_refresh_token(client):
    res = client.post("/auth/refresh")

    assert res.status_code == 422
    
    