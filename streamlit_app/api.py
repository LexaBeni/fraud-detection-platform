import requests

API_URL = "http://localhost:8000"


def predict(transaction: dict):
    response = requests.post(f"{API_URL}/predict")

    response.raise_for_status()

    return response.json()
