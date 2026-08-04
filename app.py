import streamlit as st
from auth import authenticate
from modules.dashboard import show_dashboard
from modules.admin_dashboard import show_admin_dashboard

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

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

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

        user = authenticate(username, password)

        if user:

            st.session_state.logged_in = True
            st.session_state.username = user["username"]
            st.session_state.role = user["role"]

            st.rerun()

        else:

            st.error("Invalid Username or Password")

# -----------------------------
# Dashboard
# -----------------------------
else:

    if st.session_state.role == "admin":

        show_admin_dashboard()

    else:

        show_dashboard()
