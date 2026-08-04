import streamlit as st
from auth import authenticate
from modules.dashboard import show_dashboard

st.set_page_config(
    page_title="Dealer Automation",
    page_icon="📧",
    layout="centered"
)

# -----------------------------
# Session State
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -----------------------------
# Login Page
# -----------------------------
if not st.session_state.logged_in:

    st.title("🔐 Dealer Automation Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if authenticate(username, password):

            st.session_state.logged_in = True
            st.rerun()

        else:

            st.error("Invalid Username or Password")

# -----------------------------
# Dashboard
# -----------------------------
else:

    show_dashboard()
