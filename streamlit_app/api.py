import requests
import streamlit as st

API_URL = "http://localhost:8000"


def get_auth_headers():
    token = st.session_state.get("access_token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


def register_user(email, password):
    response = requests.post(
        f"{API_URL}/auth/register", json={"email": email, "password": password}
    )
    response.raise_for_status()
    return response.json()


def login_user(username, password):
    response = requests.post(
        f"{API_URL}/auth/login", data={"username": username, "password": password}
    )

    response.raise_for_status()
    return response.json()


def predict(transaction: dict):
    response = requests.post(
        f"{API_URL}/predict", json=transaction, headers=get_auth_headers()
    )

    response.raise_for_status()

    return response.json()


def delete_prediction(id: int):
    response = requests.delete(
        f"{API_URL}/predict/delete/{id}", headers=get_auth_headers()
    )

    response.raise_for_status()

    return response.json()


def get_prediction(id: int):
    response = requests.get(
        f"{API_URL}/predict/history/{id}", headers=get_auth_headers()
    )

    response.raise_for_status()

    return response.json()


def get_history():
    response = requests.get(f"{API_URL}/predict/history", headers=get_auth_headers())

    response.raise_for_status()

    return response.json()
