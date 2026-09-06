def test_user_create(client):
    data = {"email": "test@test.com", "password": "test"}

    res = client.post("/auth/register", json=data)

    assert res.status_code == 201
    assert "password" not in res.json()
    assert res.json()['role'] == "user"
    print(res.json())