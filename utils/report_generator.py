import os
import pandas as pd

from utils.session_manager import create_session_folder


# ==================================
# Generate Safe File Name
# ==================================

def generate_filename(
    dealer_code,
    dealer_name
):

    dealer_name = (
        str(dealer_name)
        .replace("/", "_")
        .replace("\\", "_")
        .strip()
    )

    return f"{dealer_code}_{dealer_name}.xlsx"


# ==================================
# Generate Dealer Reports
# ==================================

def generate_reports(
    sales_df,
    dealer_df
):

    # Create temporary folder for current user session
    output_folder = create_session_folder()

    dealer_codes = (
        sales_df["Dealer_Code"]
        .dropna()
        .unique()
    )

    generated_reports = []

    for code in dealer_codes:

        # -------------------------
        # Dealer Sales
        # -------------------------

        dealer_sales = sales_df[
            sales_df["Dealer_Code"] == code
        ]

        # -------------------------
        # Dealer Information
        # -------------------------

        dealer_info = dealer_df[
            dealer_df["Dealer_Code"] == code
        ]

        if dealer_info.empty:

            dealer_name = "UnknownDealer"
            dealer_email = None

        else:

            dealer_name = dealer_info.iloc[0]["Dealer_Name"]
            dealer_email = dealer_info.iloc[0]["Email"]

        # -------------------------
        # Create File Name
        # -------------------------

        filename = generate_filename(
            code,
            dealer_name
        )

        output_path = os.path.join(
            output_folder,
            filename
        )

        # -------------------------
        # Save Excel File
        # -------------------------

        dealer_sales.to_excel(
            output_path,
            index=False
        )

        # -------------------------
        # Store Report Information
        # -------------------------

        generated_reports.append(
            {
                "dealer_code": code,
                "dealer_name": dealer_name,
                "email": dealer_email,
                "file": output_path
            }
        )

    return generated_reports, output_folder