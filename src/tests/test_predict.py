import pytest

def test_predict(client, auth_header):
    data = {
        "TransactionDT": 86400,
        "TransactionAmt": 49.50,
        "ProductCD": "W",
        "P_emaildomain": "gmail.com",
        "R_emaildomain": None,
        "card1": 13926,
        "card2": 327,
        "card4": "discover",
        "card5": 162,
        "card6": "credit",
        "addr1": 315,
        "addr2": 87,
        "dist1": 19.0,
        "dist2": None,
        "D1": 14.0,
    }

    res = client.post("/predict", json=data, headers=auth_header)

    assert res.status_code == 200

    result = res.json()

    assert result['prediction'] == "VALID"

@pytest.mark.parametrize("field, value", [
    ("TransactionDT", -1),
    ("TransactionAmt", -10),
    ("dist1", -1),
    ("dist2", -1),
    ("D1", -1),
])
def test_invalid_predict(client, auth_header, field, value):
    data = {
        "TransactionDT": 86400,
        "TransactionAmt": 49.50,
        "ProductCD": "W",
        "dist1": 19.0,
        "dist2": None,
        "D1": 14.0,
    }

    data[field] = value

    res = client.post("/predict", json = data, headers=auth_header)

    assert res.status_code == 422

def test_predict_without_auth(client):
    data = {
        "TransactionDT": 86400,
        "TransactionAmt": 49.50,
        "ProductCD": "W",
    }

    res = client.post("/predict", json=data)

    assert res.status_code == 401