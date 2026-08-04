import time
import pandas as pd
import streamlit as st

from utils.excel_reader import read_excel
from utils.report_generator import generate_reports
from utils.email_sender import send_email

def show_dashboard():

    st.title("📊 Dealer Automation Dashboard")

    # -------------------------------
    # Logout Button
    # -------------------------------
    if st.sidebar.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.rerun()

    st.write(
        "Upload your files and send dealer reports."
    )

    st.divider()

    # -------------------------------
    # Upload Files
    # -------------------------------

    sales_file = st.file_uploader(
        "Upload Files for Distribution",
        type=["xlsx"]
    )

    dealer_file = st.file_uploader(
        "Upload Dealer Details",
        type=["xlsx"]
    )

    st.divider()

    # -------------------------------
    # Email Credentials
    # -------------------------------

    sender_email = st.text_input(
        "Sender Gmail"
    )

    app_password = st.text_input(
        "Gmail App Password",
        type="password"
    )

    # -------------------------------
    # Read Uploaded Files
    # -------------------------------

    sales_df = None
    dealer_df = None

    if sales_file is not None:
        sales_df = read_excel(sales_file)

    if dealer_file is not None:
        dealer_df = read_excel(dealer_file)

    # -------------------------------
    # Success Messages
    # -------------------------------

    if sales_df is not None:
        st.success("Distribution File Loaded Successfully")

    if dealer_df is not None:
        st.success("Dealer Details Loaded Successfully")

    # -------------------------------
    # Preview Files
    # -------------------------------

    if sales_df is not None:
        st.subheader("Distribution Data Preview")
        st.dataframe(sales_df.head())

    if dealer_df is not None:
        st.subheader("Dealer Details Preview")
        st.dataframe(dealer_df.head())

    # -------------------------------
    # Validate Required Columns
    # -------------------------------

    required_sales_columns = [
        "Dealer_Code"
    ]

    required_dealer_columns = [
        "Dealer_Code",
        "Dealer_Name",
        "Email"
    ]

    if sales_df is not None:

        missing = [
            column
            for column in required_sales_columns
            if column not in sales_df.columns
        ]

        if missing:

            st.error(
                f"Distribution file is missing: {missing}"
            )

            st.stop()

    if dealer_df is not None:

        missing = [
            column
            for column in required_dealer_columns
            if column not in dealer_df.columns
        ]

        if missing:

            st.error(
                f"Dealer file is missing: {missing}"
            )

            st.stop()

    # -------------------------------
    # Generate Reports & Send Emails
    # -------------------------------

    if (
        sales_df is not None
        and dealer_df is not None
        and sender_email
        and app_password
    ):

        if st.button(
            "Generate Reports & Send Emails",
            use_container_width=True
        ):
            
            with st.spinner(
                "Generating reports and sending emails..."
            ):

                progress_bar = st.progress(0)

                status_text = st.empty()

                summary_placeholder = st.empty()

                results = []

                start_time = time.time()

                generated_reports, output_folder = generate_reports(
                    sales_df,
                    dealer_df
                )    

            generated_reports, output_folder = generate_reports(
                sales_df,
                dealer_df
            )
            
            total_reports = len(generated_reports)

            success_count = 0

            for report in generated_reports:

                if report["email"] is None:

                    st.warning(
                        f"No email found for {report['dealer_name']}"
                    )

                    continue

                subject = "Dealer Report"

                body = f"""
Dear {report['dealer_name']},

Please find attached your report.

Regards,
TVS Motor
"""

                try:

                    send_email(
                        sender_email,
                        app_password,
                        report["email"],
                        subject,
                        body,
                        report["file"]
                    )

                    success_count += 1

                    st.success(
                        f"Email sent to {report['dealer_name']}"
                    )

                except Exception as e:

                    st.error(
                        f"Failed to send email to {report['dealer_name']}"
                    )

                    st.exception(e)

            st.success(
                f"{success_count} email(s) sent successfully."
            )

            st.info(
                f"Reports were generated in:\n{output_folder}"
            )