"""
This module lets you save created dataframes to excel, if they've been created with the package's functions
they may contain some additional meta-data
"""
import pandas as pd


def save_to_excel(df: pd.DataFrame, filepath: str) -> None:
    """
    TODO: desc
    :param df:
    :param filepath:
    :return:
    """
    df.to_excel(filepath)
    print(f"Saved succesfully at {filepath}")
    if df.attrs['type'] == 'income_comparison':
        if not df.attrs["integrity_report"].empty:
            filepath_temp = filepath.split("/")
            file = filepath_temp[-1]
            filepath_temp[-1] = file.split(".")[0] + "_skipped." + file.split(".")[1]
            filepath_integrity = '/'.join(filepath_temp)
            df.attrs["integrity_report"].to_excel(filepath_integrity)
            print(f"Integrity check skipped-report saved at {filepath_integrity}")
    if df.attrs['type'] == 'zadanie2':
        pass
