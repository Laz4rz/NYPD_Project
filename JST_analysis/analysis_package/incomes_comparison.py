"""
Module containing functions to compare incomes for different types of JST year-to-year
"""
import pandas as pd

from .integrity import check_integrity


def compare_incomes(df1: pd.DataFrame, df2: pd.DataFrame):
    """
    This function creates a dataframe with [%] and [zł] comparison between two dataframes with PIT incomes created
    with load_income_excel(). Order of dataframes passed is important as df1 will be used as a base to calculate change.
    :param df1: Base income dataframe to create comparison
    :param df2: Income dataframe to compoare with df1
    :return: pd.Dataframe with summarised informations about the comparison
    """
    df1_JST_type = df1.attrs["JST_type"]
    df2_JST_type = df2.attrs["JST_type"]
    df1_type = df1.attrs["type"]
    df2_type = df2.attrs["type"]
    if df1.attrs["JST_type"] != df2.attrs["JST_type"]:
        raise Exception(
            f"JST types of dataframes dont match, df1: {df1_JST_type}, df2: {df2_JST_type}"
        )
    elif df1_type == df2_type == "base_income":
        raise Exception(
            f"dataframes have to be of base_income type, df1: {df1_type}, df2: {df2_type}"
        )
    else:
        integrity_report = check_integrity(df1=df1, df2=df2, mode="compare_incomes")
        df = create_base_compare_df(df1=df1, df2=df2)
        df.attrs["integrity_report"] = integrity_report
        df.attrs["year"] = [df1.attrs["year"], df2.attrs["year"]]
        df = calculate_comparison(df=df)
        return df


def create_base_compare_df(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    df = df1[df1[df1.attrs["JST_type"]] == df2[df2.attrs["JST_type"]]][
        [
            "Kod",
            df1.attrs["JST_type"],
            "województwo",
            "powiat",
            "Dochody PIT",
        ]
    ]
    df = df.rename(columns={"Dochody PIT": f"Dochody w {df1.attrs['year']}"})

    df2_income = df2[df1[df1.attrs["JST_type"]] == df2[df2.attrs["JST_type"]]][
        "Dochody PIT"
    ]
    df[f"Dochody w {df2.attrs['year']}"] = df2_income

    df.attrs["type"] = "income_comparison"
    return df


def calculate_comparison(df: pd.DataFrame) -> pd.DataFrame:
    col1 = df[f'Dochody w {df.attrs["year"][0]}'].astype(float)
    col2 = df[f'Dochody w {df.attrs["year"][1]}'].astype(float)
    df[f'Różnica {df.attrs["year"][0]}/{df.attrs["year"][1]}[%]'] = percentage_change(
        col1=col1, col2=col2
    ).map(lambda x: "{:.2f}".format(round(x, 2)))
    df[f'Różnica {df.attrs["year"][0]}/{df.attrs["year"][1]}[zł]'] = (col2 - col1).map(
        lambda x: "{:.2f}".format(round(x, 2))
    )
    return df


def percentage_change(col1: pd.Series, col2: pd.Series) -> pd.Series:
    return ((col2 - col1) / col1) * 100
