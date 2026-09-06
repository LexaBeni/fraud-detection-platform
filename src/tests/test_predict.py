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
