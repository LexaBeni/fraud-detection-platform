import streamlit as st

from streamlit_app.api import (
    delete_prediction,
    get_history,
    get_prediction,
    login_user,
    predict,
    register_user,
)

st.set_page_config(page_title="Fraud Detection", layout="wide")

if "access_token" not in st.session_state:
    st.session_state["access_token"] = None

if "refresh_token" not in st.session_state:
    st.session_state["refresh_token"] = None

if not st.session_state["access_token"]:
    st.title("Fraud Detection System - Login")
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1, st.form("login"):
        username = st.text_input("Email")
        password = st.text_input("Password")
        if st.form_submit_button("Login"):
            data = login_user(username, password)
            st.session_state["access_token"] = data["access_token"]
            st.session_state["refresh_token"] = data["refresh_token"]
            st.success("Successfully logged in!")
            st.rerun()
    with tab2, st.form("Register"):
        email = st.text_input("Email")
        password = st.text_input("Password")
        if st.form_submit_button("Register"):
            register_user(email, password)
            st.success("Registration successful! Please login.")

else:
    with st.sidebar:
        st.success("Logged in")
        page = st.radio("Page", ["Prediction", "History"])
        if st.button("Log out"):
            st.session_state["access_token"] = None
            st.session_state["refresh_token"] = None
            st.rerun()

    if page == "Prediction":
        st.title("Fraud Detection")

        st.write("Detect potentially fraudulent transactions using machine learning.")

        st.divider()

        with st.form("Prediction form"):
            transaction_dt = st.number_input("TransactionDT", min_value=0)
            transaction_amt = st.number_input("TransactionAmt", min_value=0, value=100)
            product_cd = st.selectbox("ProductCD", options=["W", "C", "R", "H", "S"])
            p_emaildomain = st.text_input("P_emaildomain")
            r_emaildomain = st.text_input("R_emaildomain")
            p_emaildomain = p_emaildomain or None
            r_emaildomain = r_emaildomain or None
            card4 = st.selectbox(
                "card4",
                options=["visa", "mastercard", "american express", "discover", None],
            )
            card6 = st.selectbox(
                "card6",
                options=["credit", "debit", "debit or credit", "charge card", None],
            )

            def nullable_number_input(label, min_value=0):
                is_missing = st.checkbox(f"{label} is missing", value=True)

                if is_missing:
                    return None

                return st.number_input(label, min_value=min_value)

            card1 = nullable_number_input("card1", min_value=1000)
            card2 = nullable_number_input("card2", min_value=100)
            card5 = nullable_number_input("card5", min_value=100)

            addr1 = nullable_number_input("addr1")
            addr2 = nullable_number_input("addr2")
            dist1 = nullable_number_input("dist1")
            dist2 = nullable_number_input("dist2")
            d1 = nullable_number_input("D1")

            button = st.form_submit_button("Submit")
            if button:
                transaction = {
                    "TransactionDT": transaction_dt,
                    "TransactionAmt": transaction_amt,
                    "ProductCD": product_cd,
                    "P_emaildomain": p_emaildomain,
                    "R_emaildomain": r_emaildomain,
                    "card1": card1,
                    "card2": card2,
                    "card4": card4,
                    "card5": card5,
                    "card6": card6,
                    "addr1": addr1,
                    "addr2": addr2,
                    "dist1": dist1,
                    "dist2": dist2,
                    "D1": d1,
                }

                result = predict(transaction)

                st.json(result)

    if page == "History":
        st.title("Prediction History")
        st.write("Select or delete your prediction.")
        with st.form("Specific History Form"):
            st.subheader("Select your specific prediction.")
            id = st.number_input("Prediction ID", min_value=0, step=1)
            if st.form_submit_button("Get prediction"):
                result = get_prediction(int(id))
                st.dataframe(result)

        with st.form("History Form"):
            st.subheader("See all your predictions.")
            if st.form_submit_button("Get all predictions"):
                result = get_history()
                st.dataframe(result)
        with st.form("Delete Form"):
            st.subheader("Delete your prediction")
            id = st.number_input("Prediction id", min_value=0, step=1)
            if st.form_submit_button(f"Delete prediction with id {id}"):
                result = delete_prediction(id)
                st.dataframe(result)
