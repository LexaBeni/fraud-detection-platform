import requests
import streamlit as st

API_URL = "http://localhost:8000"


class AuthenticationError(Exception):
    pass


def token(refresh_token: str):
    response = requests.post(
        f"{API_URL}/auth/refresh", json={"refresh_token": refresh_token}
    )
    if response.status_code == 401:
        st.session_state["refresh_token"] = None
        st.session_state["access_token_token"] = None
        return AuthenticationError("Session expired.")

    response.raise_for_status()
    data = response.json()
    st.session_state["refresh_token"] = data["refresh_token"]
    st.session_state["access_token"] = data["access_token"]


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

    if response.status_code == 401:
        token(st.session_state["refresh_token"])
        response = requests.post(
            f"{API_URL}/predict", json=transaction, headers=get_auth_headers()
        )
    response.raise_for_status()
    return response.json()


def delete_prediction(id: int):
    response = requests.delete(
        f"{API_URL}/predict/delete/{id}", headers=get_auth_headers()
    )

    if response.status_code == 401:
        token(st.session_state["refresh_token"])
        response = requests.delete(
            f"{API_URL}/predict/delete/{id}", headers=get_auth_headers()
        )
    response.raise_for_status()

    return response.json()


def get_prediction(id: int):
    response = requests.get(
        f"{API_URL}/predict/history/{id}", headers=get_auth_headers()
    )

    if response.status_code == 401:
        token(st.session_state["refresh_token"])
        response = requests.get(
            f"{API_URL}/predict/history/{id}", headers=get_auth_headers()
        )
    response.raise_for_status()

    return response.json()


def get_history():
    response = requests.get(f"{API_URL}/predict/history", headers=get_auth_headers())

    if response.status_code == 401:
        token(st.session_state["refresh_token"])
        response = requests.get(
            f"{API_URL}/predict/history", headers=get_auth_headers()
        )
    response.raise_for_status()

    return response.json()
