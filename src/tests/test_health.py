def test_health(client):
    res = client.get("/health")

    data = res.json()

    assert res.status_code == 200
    assert data["status"] == "healthy"
    assert data["model"] == "ok"
    assert data["database"] == "ok"
