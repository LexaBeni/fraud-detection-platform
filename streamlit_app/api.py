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
        st.session_state["access_token"] = None
        raise AuthenticationError("Session expired.")

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


def request(method, endpoint, **kwargs):
    response = requests.request(
        method, f"{API_URL}{endpoint}", **kwargs, headers=get_auth_headers()
    )
    if response.status_code == 401:
        refresh_token = st.session_state.get("refresh_token")
        if not refresh_token:
            raise ValueError("No refresh token available.")
        token(refresh_token)
        response = requests.request(
            method, f"{API_URL}{endpoint}", **kwargs, headers=get_auth_headers()
        )

    response.raise_for_status()
    return response.json()


def predict(transaction: dict):
    return request("POST", "/predict", json=transaction)


def delete_prediction(prediction_id: int):
    return request("DELETE", f"/predict/delete/{prediction_id}")


def get_prediction(prediction_id: int):
    return request("GET", f"/predict/history/{prediction_id}")


def get_history():
    return request("GET", "/predict/history")
