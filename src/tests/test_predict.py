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

    assert result['prediction'] == "FRAUD"
    assert result['probability'] == 0.9
    assert "id" in result
    assert result["threshold"] == 0.18
    assert isinstance(result["created_at"], str)

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

def test_get_prediction(client, create_prediction, auth_header):
    prediction_id = create_prediction['id']

    res = client.get(f"/predict/history/{prediction_id}", headers = auth_header)

    data = res.json()

    assert res.status_code == 200
    assert data['id'] == prediction_id
    assert data['created_at'] is not None
    assert data['threshold'] == 0.18
    assert data['prediction'] in ["FRAUD", "VALID"]
    assert data['probability'] <= 1

def test_get_prediction_no_auth(client, create_prediction):
    prediction_id = create_prediction["id"]

    res = client.get(f"/predict/history/{prediction_id}")

    assert res.status_code == 401

def test_get_history(client, create_prediction, auth_header):
    res = client.get("/predict/history", headers=auth_header)

    prediction_id = create_prediction['id']

    data = res.json()[0]

    assert res.status_code == 200
    assert data['id'] == prediction_id
    assert data['created_at'] is not None
    assert data['threshold'] == 0.18
    assert data['prediction'] in ["FRAUD", "VALID"]
    assert data['probability'] <= 1

def test_get_prediction_admin(client, create_prediction, auth_admin):
    prediction_id = create_prediction["id"]
    res = client.get(f"/predict/history/{prediction_id}", headers=auth_admin)

    assert res.status_code == 200

    data = res.json()

    assert data['id'] == prediction_id
    assert data['created_at'] is not None
    assert data['threshold'] == 0.18
    assert data['prediction'] in ["FRAUD", "VALID"]
    assert data['probability'] <= 1

def test_get_another_user_predicttion(client, create_prediction, another_auth_header):
    prediction_id = create_prediction["id"]

    res = client.get(f"/predict/history/{prediction_id}", headers=another_auth_header)

    assert res.status_code == 404
    
    data = res.json() 
    assert data["error_code"] == "PREDICTION_NOT_FOUND"

def test_delete_prediction(client, create_prediction, auth_header):
    prediction_id = create_prediction["id"]
    
    res = client.delete(f"/predict/delete/{prediction_id}", headers=auth_header)

    assert res.status_code == 200

    data = res.json()

    assert data == (f"The prediction with id {prediction_id} was successfully removed.")

    res = client.get(f"/predict/history/{prediction_id}", headers=auth_header)

    assert res.status_code == 404

def test_delete_prediction_no_auth(client, create_prediction):
    prediction_id = create_prediction["id"]

    res = client.delete(f"/predict/delete/{prediction_id}")

    assert res.status_code == 401

def test_delete_prediction_not_found(client, auth_header):

    res = client.delete("/predict/delete/999", headers=auth_header)

    assert res.status_code == 404

    data = res.json()

    assert data["status"] == "error"
    assert data["error_code"] == "PREDICTION_NOT_FOUND"

def test_admin_delete_prediction(client, create_prediction, auth_admin):
    prediction_id = create_prediction["id"]

    res = client.delete(f"/predict/delete/{prediction_id}", headers=auth_admin)

    assert res.status_code == 200

    res = client.get(f"/predict/history/{prediction_id}",headers=auth_admin)

    assert res.status_code == 404

def test_delete_other_user_prediction(client, create_prediction, another_auth_header):
    prediction_id = create_prediction["id"]

    res = client.delete(f"/predict/delete/{prediction_id}", headers=another_auth_header)

    assert res.status_code == 404