import streamlit as st

st.set_page_config(page_title="Fraud Detection", layout="wide")

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
        "card4", options=["visa", "mastercard", "american express", "discover", None]
    )
    card6 = st.selectbox(
        "card6", options=["credit", "debit", "debit or credit", "charge card", None]
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
        st.success("Fine")
