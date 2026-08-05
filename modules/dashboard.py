import time
import shutil
import streamlit as st

from utils.excel_reader import read_excel
from utils.report_generator import generate_reports
from utils.email_sender import send_email
from utils.logger import log_usage


def show_dashboard():

    # ======================================================
    # Page Title
    # ======================================================

    st.title("📊 Dealer Report Automation ")

    # Instructions
    st.info("""
    📌 **Upload Instructions**

    - **Dealer Distribution File (.xlsx):** Must contain a **Dealer_Code** column with values matching the Dealer Details file.
    - **Dealer Details File (.xlsx):** Must contain **Dealer_Code**, **Dealer_Name**, and **Email** columns.
    - Keep the column names exactly as specified and do not leave mandatory fields blank.
    - File names can be anything, but both files must be in **.xlsx** format and have matching **Dealer_Code** values.
    """)


    st.sidebar.markdown(f"### 👋 Welcome {st.session_state.username}")


    # ======================================================
    # Logout
    # ======================================================

    if st.sidebar.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.rerun()

    st.write(
        "Upload your distribution file and dealer details file to generate dealer-wise reports and send them via email."
    )

    st.divider()

    # ======================================================
    # Upload Files
    # ======================================================

    sales_file = st.file_uploader(
        "Upload Distribution File",
        type=["xlsx"]
    )

    dealer_file = st.file_uploader(
        "Upload Dealer Details",
        type=["xlsx"]
    )

    st.divider()

    # ======================================================
    # Email Credentials
    # ======================================================

    sender_email = st.text_input(
        "Sender Gmail"
    )

    app_password = st.text_input(
        "Gmail App Password",
        type="password"
    )

    # ======================================================
    # Read Files
    # ======================================================

    sales_df = None
    dealer_df = None

    if sales_file is not None:
        sales_df = read_excel(sales_file)

    if dealer_file is not None:
        dealer_df = read_excel(dealer_file)

    # ======================================================
    # Success Messages
    # ======================================================

    if sales_df is not None:
        st.success("✅ Distribution File Loaded Successfully")

    if dealer_df is not None:
        st.success("✅ Dealer Details Loaded Successfully")

    # ======================================================
    # Preview
    # ======================================================

    if sales_df is not None:

        with st.expander("Distribution File Preview"):

            st.dataframe(
                sales_df.head(),
                use_container_width=True
            )

    if dealer_df is not None:

        with st.expander("Dealer Details Preview"):

            st.dataframe(
                dealer_df.head(),
                use_container_width=True
            )

    # ======================================================
    # Validate Columns
    # ======================================================

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
            c
            for c in required_sales_columns
            if c not in sales_df.columns
        ]

        if missing:

            st.error(
                f"Distribution File Missing Columns : {missing}"
            )

            st.stop()

    if dealer_df is not None:

        missing = [
            c
            for c in required_dealer_columns
            if c not in dealer_df.columns
        ]

        if missing:

            st.error(
                f"Dealer File Missing Columns : {missing}"
            )

            st.stop()

    # ======================================================
    # Generate Reports & Send Emails
    # ======================================================

    if (
        sales_df is not None
        and dealer_df is not None
        and sender_email
        and app_password
    ):

        if st.button(
            "🚀 Generate Reports & Send Emails",
            use_container_width=True
        ):

            # ===============================================
            # Stage 1
            # ===============================================

            st.subheader("📄 Stage 1 : Report Generation")

            stage1_status = st.empty()

            with st.spinner("Generating Dealer Reports..."):

                stage1_status.info(
                    "Generating Excel Reports..."
                )

                start_generation = time.time()

                generated_reports, output_folder = generate_reports(
                    sales_df,
                    dealer_df
                )

                generation_time = (
                    time.time() - start_generation
                )

            stage1_status.success(
                f"✅ Successfully Generated {len(generated_reports)} Reports"
            )

            st.info(
                f"Generation Time : {generation_time:.2f} seconds"
            )

            st.divider()

            # ===============================================
            # Stage 2 : Send Emails
            # ===============================================

            st.subheader("📧 Stage 2 : Sending Emails")

            progress_bar = st.progress(0)

            processed_text = st.empty()
            dealer_text = st.empty()
            email_text = st.empty()

            col1, col2, col3 = st.columns(3)

            success_metric = col1.empty()
            failed_metric = col2.empty()
            skipped_metric = col3.empty()

            elapsed_text = st.empty()
            eta_text = st.empty()

            total_reports = len(generated_reports)

            processed = 0
            success_count = 0
            failed_count = 0
            skipped_count = 0

            start_time = time.time()

            for report in generated_reports:

                processed += 1

                progress = processed / total_reports

                progress_bar.progress(progress)

                processed_text.markdown(
                    f"### {processed} / {total_reports} Dealers Processed"
                )

                dealer_text.write(
                    f"**Current Dealer :** {report['dealer_name']}"
                )

                email_text.write(
                    f"**Current Email :** {report['email'] if report['email'] else 'No Email Available'}"
                )

                elapsed = time.time() - start_time

                avg_time = elapsed / processed

                eta = avg_time * (total_reports - processed)

                elapsed_text.write(
                    f"⏱ Elapsed Time : {int(elapsed // 60)}m {int(elapsed % 60)}s"
                )

                eta_text.write(
                    f"⌛ Estimated Time Remaining : {int(eta // 60)}m {int(eta % 60)}s"
                )

                # -----------------------------------
                # No Email
                # -----------------------------------

                if report["email"] is None:

                    skipped_count += 1

                    success_metric.metric(
                        "Success",
                        success_count
                    )

                    failed_metric.metric(
                        "Failed",
                        failed_count
                    )

                    skipped_metric.metric(
                        "Skipped",
                        skipped_count
                    )

                    continue

                subject = "Dealer Report"

                body = f"""
            Dear {report['dealer_name']},

            Please find attached your Dealer Report.

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

                except Exception:

                    failed_count += 1

                success_metric.metric(
                    "Success",
                    success_count
                )

                failed_metric.metric(
                    "Failed",
                    failed_count
                )

                skipped_metric.metric(
                    "Skipped",
                    skipped_count
                )

            # ===============================================
            # Completed
            # ===============================================

            progress_bar.progress(1.0)

            total_time = time.time() - start_time

            st.divider()

            st.success("🎉 Dealer Automation Completed Successfully")

            summary1, summary2, summary3, summary4 = st.columns(4)

            summary1.metric(
                "Total",
                total_reports
            )

            summary2.metric(
                "Success",
                success_count
            )

            summary3.metric(
                "Failed",
                failed_count
            )

            summary4.metric(
                "Skipped",
                skipped_count
            )

            st.info(
                f"""
            📁 Reports Location

            {output_folder}
            """
            )

            st.write(
                f"**Total Email Processing Time :** {int(total_time//60)}m {int(total_time%60)}s"
            )

            log_usage(
                username=st.session_state.username,
                reports=total_reports,
                emails_sent=success_count,
                success=success_count,
                failed=failed_count,
                skipped=skipped_count,
                duration=total_time
            )

            # ===============================================
            # Delete Temporary Files
            # ===============================================

            try:

                shutil.rmtree(output_folder)

                st.success("🗑️ Temporary files deleted successfully.")

            except Exception as e:

                st.warning(
                    f"Could not delete temporary files: {e}"
                )