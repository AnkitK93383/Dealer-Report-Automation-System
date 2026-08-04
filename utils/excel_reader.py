import pandas as pd


def read_excel(uploaded_file):
    """
    Reads an uploaded Excel file
    and returns a pandas DataFrame.
    """

    dataframe = pd.read_excel(uploaded_file)

    return dataframe