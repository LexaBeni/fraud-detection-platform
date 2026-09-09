from contextlib import asynccontextmanager

import numpy as np
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.api.core.database import Base
from src.api.core.settings import settings
from src.api.main import app
from src.api.services.bootstrap_service import ensure_admin
from src.dependencies.database import get_db

test_engine = create_engine(settings.test_database_url)

test_session_local = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)

def override_get_db():
    db = test_session_local()

    try:
        yield db

    finally:
        db.close()

class DummyModel:
    def predict(self, X):
        return np.array([1])
    def predict_proba(self, X):
        return np.array([[0.1, 0.9]])

@asynccontextmanager
async def test_lifespan(app):
    app.state.model = DummyModel()
    yield

@pytest.fixture
def client():

    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    app.dependency_overrides[get_db] = override_get_db
    original_lifespan = app.router.lifespan_context
    app.router.lifespan_context = test_lifespan

    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.router.lifespan_context = original_lifespan

    app.dependency_overrides.clear()

@pytest.fixture
def user_create(client):
    data = {"email": "test@test.com", "password": "test"}

    res = client.post("/auth/register", json=data)

    user = res.json()

    assert res.status_code == 201

    user['password'] = data['password']

    return user

@pytest.fixture
def another_user_create(client):
    data = {"email": "test2@test.com", "password": "test2"}

    res = client.post("/auth/register", json=data)

    user = res.json()

    assert res.status_code == 201

    user['password'] = data['password']

    return user

@pytest.fixture
def create_admin(client):
    db = test_session_local()
    try:
        return ensure_admin(db)
    finally:
        db.close()

@pytest.fixture
def user_login(client, user_create):

    res = client.post("/auth/login", data = {"username": user_create['email'], "password": user_create['password']})

    tokens = res.json()

    assert res.status_code == 200

    return tokens

@pytest.fixture
def another_user_login(client, another_user_create):

    res = client.post("/auth/login", data = {"username": another_user_create['email'], "password": another_user_create['password']})

    tokens = res.json()

    assert res.status_code == 200

    return tokens

@pytest.fixture
def login_admin(client, create_admin):
    res = client.post("/auth/login", data={"username": create_admin.email, "password": settings.admin_password})

    assert res.status_code == 200

    return res.json()

@pytest.fixture
def auth_header(user_login):
    return {"Authorization": f"Bearer {user_login["access_token"]}"}

@pytest.fixture
def another_auth_header(another_user_login):
    return {"Authorization": f"Bearer {another_user_login["access_token"]}"}

@pytest.fixture
def auth_admin(login_admin):
    return {"Authorization": f"Bearer {login_admin["access_token"]}"}

@pytest.fixture
def create_prediction(client, auth_header):
    data = {
        "TransactionDT": 86400,
        "TransactionAmt": 49.50,
        "ProductCD": "W"
    }

    res = client.post("/predict", json=data, headers=auth_header)

    assert res.status_code == 200

    result = res.json()

    return result
    