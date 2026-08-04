import pandas as pd
import streamlit as st
from datetime import datetime

LOG_FILE = "logs/usage_log.csv"


def show_admin_dashboard():

    st.title("🛠 Admin Dashboard")

    st.sidebar.success(
        f"Welcome {st.session_state.username}"
    )

    if st.sidebar.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""

        st.rerun()

    try:

        df = pd.read_csv(LOG_FILE)
        # Convert Date column to datetime
        df["Date"] = pd.to_datetime(
            df["Date"],
            format="%d-%m-%Y"
)

        # ==========================================
        # Sidebar Filters
        # ==========================================

        st.sidebar.header("🔍 Filters")

        # -------------------------
        # User Filter
        # -------------------------

        selected_user = st.sidebar.selectbox(

            "Select User",

            ["All"] + sorted(df["Username"].unique())

        )

        # -------------------------
        # Date Range Filter
        # -------------------------

        min_date = df["Date"].min().date()

        max_date = df["Date"].max().date()

        date_range = st.sidebar.date_input(

            "Select Date Range",

            value=(min_date, max_date),

            min_value=min_date,

            max_value=max_date

        )

        # -------------------------
        # Apply User Filter
        # -------------------------

        if selected_user != "All":

            df = df[df["Username"] == selected_user]

        # -------------------------
        # Apply Date Range Filter
        # -------------------------

        if len(date_range) == 2:

            start_date, end_date = date_range

            df = df[
                (df["Date"] >= pd.Timestamp(start_date))
                &
                (df["Date"] <= pd.Timestamp(end_date))
            ]


    except FileNotFoundError:

        st.warning("No usage logs found.")

        return

    # ==========================================
    # Total Usage
    # ==========================================

    st.subheader("📊 Total Usage")

    total_users = df["Username"].nunique()

    total_reports = df["Reports"].sum()

    total_emails = df["Emails Sent"].sum()

    total_success = df["Success"].sum()

    total_failed = df["Failed"].sum()

    total_time = len(df)

    col1, col2, col3 = st.columns(3)

    col4, col5, col6 = st.columns(3)

    with col1:
        st.metric(
            "👥 Users",
            total_users
        )

    with col2:
        st.metric(
            "📄 Reports",
            total_reports
        )

    with col3:
        st.metric(
            "📧 Emails",
            total_emails
        )

    with col4:
        st.metric(
            "✅ Success",
            total_success
        )

    with col5:
        st.metric(
            "❌ Failed",
            total_failed
        )

    with col6:
        st.metric(
            "🕒 Total Runs",
            total_time
        )

    st.divider()

    # ==========================================
    # User Activity
    # ==========================================

    st.subheader("👤 User Activity")

    user_activity = (
        df.groupby("Username")
        .agg(
            Reports=("Reports", "sum"),
            Emails=("Emails Sent", "sum"),
            Success=("Success", "sum"),
            Failed=("Failed", "sum"),
            Skipped=("Skipped", "sum")
        )
        .reset_index()
    )

    st.dataframe(
        user_activity,
        use_container_width=True
    )

    st.divider()

    # ==========================================
    # Emails Sent
    # ==========================================

    st.subheader("📧 Emails Sent")

    emails = (
        df.groupby("Username")["Emails Sent"]
        .sum()
        .reset_index()
    )

    st.bar_chart(
        emails.set_index("Username")
    )

    st.divider()

    df["Date"] = df["Date"].dt.strftime("%d-%m-%Y")

    # ==========================================
    # Recent Activity
    # ==========================================

    st.subheader("🕒 Recent Activity")

    recent_activity = (
        df.sort_values(
            by=["Date", "Time"],
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        recent_activity,
        use_container_width=True
    )