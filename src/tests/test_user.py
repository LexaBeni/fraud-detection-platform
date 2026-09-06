import pytest

@pytest.fixture
def user_create(client):
    data = {"email": "test@test.com", "password": "test"}

    res = client.post("/auth/register", json=data)

    user = res.json()

    assert res.status_code == 201
    assert "password" not in user
    assert user['role'] == "user"

    user['password'] = data['password']

    return user

@pytest.fixture
def user_login(client, user_create):

    res = client.post("/auth/login", data = {"username": user_create['email'], "password": user_create['password']})

    tokens = res.json()

    assert res.status_code == 200
    assert "refresh_token" in tokens
    assert "access_token" in tokens
    assert tokens["token_type"] == "bearer"

    return tokens