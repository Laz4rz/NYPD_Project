"""
This module lets you do basic operations on the population and population-income data.
"""
import pandas as pd

from .integrity import check_integrity


def calculate_JST(df: pd.DataFrame, JST_type: str) -> pd.DataFrame:
    """
    Call it on "income-population" type dataframe to calculate variance and mean for JSTs under JST specified in
    JST_type param. You can always check your's dataframe type, by .attrs['type'].
    :param df: "income-population" type dataframe
    :param JST_type: set "powiat" or "województwo", depending on which structre you're interested in
    :return: 'mean-variance' type of df
    """
    if JST_type == "powiat":
        df2 = pd.DataFrame()
        df2["Wariancja dochodu opodatkowanego"] = df.groupby(by="powiat").agg(
            {"Dochody PIT": "var"}
        )
        df2["Średni dochód opodatkowany"] = df.groupby(by="powiat").agg(
            {"Dochody PIT": "mean"}
        )
        return df2
    elif JST_type == "województwo":
        df2 = pd.DataFrame()
        df2["Dochody PIT"] = df.groupby(by=["województwo", "powiat"]).agg(
            {"Dochody PIT": "sum"}
        )
        df2 = df2.reset_index()
        df3 = pd.DataFrame()
        df3["Wariancja dochodu opodatkowanego"] = df2.groupby(by="województwo").agg(
            {"Dochody PIT": "var"}
        )
        df3["Średni dochód opodatkowany"] = df2.groupby(by="województwo").agg(
            {"Dochody PIT": "mean"}
        )
        print("dupa")
        return df3


def calculate_tax_mean(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function lets you add a mean of tax income to the "income-population" type of dataframe. You can always check
    your's dataframe type, by .attrs['type'].
    :param df: "income-population" type dataframe
    :return: df with "Średni dochód opodatkowany" column
    """
    df["Średni dochód opodatkowany"] = df["Dochody PIT"] / df["Populacja"]
    return df


def population_income_merge(
    gmina_income_df: pd.DataFrame, populations_df: pd.DataFrame
) -> pd.DataFrame:
    """
    This function lets you merge "base_income" type/"Gminy" JST_type of dataframe and "populations" type of dataframe.
    You can always check if dataframe has a type set, by calling .attrs['type']/.attrs['JST_type'] on it.
    :param gmina_income_df: dataframe of "base_income" type/"Gminy" JST_type
    :param populations_df: dataframe of "populations" type/"Gminy" JST_type
    :return: gmina_income_df with "Populacja" column
    """
    df1 = gmina_income_df
    df2 = populations_df
    df1_type = gmina_income_df.attrs["type"]
    df2_type = populations_df.attrs["type"]
    if df1_type == "base_income" and df2_type == "populations":
        raise Exception(
            f"types of dataframes dont match, df1: {df1_type}, df2: {df2_type}"
        )
    else:
        integrity_report = check_integrity(df1=df1, df2=df2, mode="merge")
        df = expand_to_population_column(df1=df1, df2=df2)
        df.attrs["integrity_report"] = integrity_report
        df.attrs["type"] = "income-population"
    return df


def expand_to_population_column(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    merge_columns = ["Kod", "Gminy", "województwo"]
    df = df1.merge(df2.drop_duplicates(), on=merge_columns, how="left", indicator=True)
    df = df[df["_merge"] == "both"]
    df = df.drop(columns="_merge")
    return df
