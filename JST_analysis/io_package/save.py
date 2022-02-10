"""
This module lets you save created dataframes to excel, if they've been created with the package's functions
they may contain some additional meta-data
"""
import pandas as pd


def save(df: pd.DataFrame, file_path: str) -> None:
    df.to_excel(file_path)
    print(f"Saved succesfully at {file_path}")


def integrity_report_save(df, file_path) -> None:
    if not df.attrs["integrity_report"].empty:
        filepath_temp = file_path.split("/")
        file = filepath_temp[-1]
        filepath_temp[-1] = (
            file.split(".")[0] + f"_skipped_{df.attrs['type']}." + file.split(".")[1]
        )
        filepath_integrity = "/".join(filepath_temp)
        df.attrs["integrity_report"].to_excel(filepath_integrity)
        print(f"Integrity check skipped-report saved at {filepath_integrity}")


def save_to_excel(df: pd.DataFrame, file_path: str) -> None:
    """
    This function lets you save a dataframe to excel, if the dataframe was created with a function from the package it
    may additionaly save an integrity report with records skipped during integrity_check.
    :param df: df you wish to save
    :param file_path: filepath with excel file format at the end (i.e. file.xlsx)
    :return: None
    """
    save(df=df, file_path=file_path)
    if "integrity_report" in df.attrs.keys():
        integrity_report_save(df=df, file_path=file_path)
