"""
Module containing functions to load the xls file
"""

import pandas as pd

from .tax_rate import get_tax_rate

JST_types = {
    "NPP": "NPP",
    "Gminy": "Gminy",
    "Województwa": "Województwa",
    "Powiaty": "Powiaty",
    "Wojewodztwa": "Województwa",
}


def merge_territorial_code(df: pd.DataFrame) -> pd.DataFrame:
    codes = df.filter(regex="WK|PK|GK|GT", axis=1)
    df["Kod"] = codes.iloc[:, 0]
    for i in range(1, len(codes.columns)):
        df["Kod"] += codes.iloc[:, i]
    return df


def normalize_JST_names(df: pd.DataFrame) -> pd.DataFrame:
    df[df.attrs["JST_type"]] = df[df.attrs["JST_type"]].str.lower()
    return df


def clean_columns_names(df: pd.DataFrame) -> pd.DataFrame:
    for column in df.columns:
        column_name = "".join(df[column][:6].dropna().tolist())
        df = df.rename(columns={column: column_name})
    df = df.iloc[6:]
    column_name = df.filter(regex="Dochody").columns.values[0]
    df = df.rename(columns={column_name: "Dochody PIT"})
    return df.reset_index()


def drop_na_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(axis=1, how="all")


def only_important_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.filter(
        regex=f"Dochody|{df.attrs['JST_type']}|Kod|województwo|powiat", axis=1
    )


def set_JST_type(df: pd.DataFrame, file_path: str) -> pd.DataFrame:
    file_name = file_path.split("/")[-1]
    for JST_type in JST_types.keys():
        if JST_type in file_name:
            column = df.filter(like="JST").columns.values[0]
            df = df.rename(columns={column: JST_types[JST_type]})
            df.attrs["JST_type"] = JST_types[JST_type]
            return df
    print("Couldnt match file_path to any JST type from list")


def get_year(file_path: str) -> str:
    years = ["2019", "2020"]
    file_name = file_path.split("/")[-1]
    for year in years:
        if year in file_name:
            return year
    print("Couldnt match file_path to any year with tax rate saved")


def set_columns_order(df: pd.DataFrame) -> pd.DataFrame:
    return df[["Kod", df.attrs["JST_type"], "województwo", "powiat", "Dochody PIT"]]


def set_and_apply_tax_rate(
    df: pd.DataFrame, year: int, tax_rate: float, file_path: str
) -> pd.DataFrame:
    if df.attrs["JST_type"] == "NPP":
        if year is None:
            df.attrs["year"] = get_year(file_path=file_path)
        else:
            df.attrs["year"] = year
        tax_rate_75621 = get_tax_rate(df.attrs["year"], df.attrs["JST_type"], "75621")
        tax_rate_75622 = get_tax_rate(df.attrs["year"], df.attrs["JST_type"], "75622")
        df.attrs["tax_rate"] = [{"75621": tax_rate_75621}, {"75622": tax_rate_75622}]

        df_75621 = (
            df[df["ROZDZIAŁ"] == 75621]["Dochody PIT"].reset_index() * tax_rate_75621
        )
        df_75622 = (
            df[df["ROZDZIAŁ"] == 75622]["Dochody PIT"].reset_index() * tax_rate_75622
        )

        df = df.drop_duplicates(subset=["NPP"]).reset_index()

        df_total = df_75621 + df_75622
        df["Dochody PIT"] = df_total["Dochody PIT"].map(
            lambda x: "{:.2f}".format(round(x, 2))
        )
    else:
        if year is None and tax_rate is None:
            df.attrs["year"] = get_year(file_path=file_path)
            df.attrs["tax_rate"] = get_tax_rate(
                year=df.attrs["year"], JST_type=df.attrs["JST_type"]
            )
        elif year is None:
            df.attrs["tax_rate"] = tax_rate
        elif tax_rate is None:
            df.attrs["year"] = year
            df.attrs["tax_rate"] = get_tax_rate(
                year=df.attrs["year"], JST_type=df.attrs["JST_type"]
            )
        df["Dochody PIT"] *= df.attrs["tax_rate"]
    return df


def sum_NPP_income(df: pd.DataFrame) -> pd.DataFrame:
    df_sum = df.groupby(["Kod"])[["Dochody PIT"]].agg("sum").reset_index()
    df = df.drop_duplicates(subset=["NPP"]).reset_index()
    df["Dochody PIT"] = df_sum["Dochody PIT"]
    return df


def load_excel(
    file_path: str,
    sheet_name: str = 0,
    only_important: bool = False,
    JST_type: str = None,
    year: int = None,
    tax_rate: float = None,
) -> pd.DataFrame:
    """
    This function lets you load an Excel file. It will try to clean it and set correct column names if the file's
    matches expected format (i.e. 2020 JST income file).
    :param file_path: path to the excel file you wish to load
    :param sheet_name: if the file contains different sheets, you can specify which one to try and load
    :param only_important: filter columns to the ones important for the analysis
    :param JST_type: choose which JST data the file contains ['NPP', 'Gminy', 'Powiaty', 'Województwa'], by default will
    try to search file_path for information
    :param year: year from which the data comes, will try and match it with correct tax rate for JST type
    :param tax_rate: use to override automatic tax rate, if you wish to compare JST/year that isn't stored in the
    package
    :return: pd.DataFrame object
    """
    df = pd.read_excel(io=file_path, sheet_name=sheet_name)
    df = clean_columns_names(df=df)
    df = drop_na_columns(df=df)
    df = merge_territorial_code(df=df)

    if JST_type is None:
        df = set_JST_type(df=df, file_path=file_path)

    df = normalize_JST_names(df=df)

    df = set_and_apply_tax_rate(
        df=df, year=year, tax_rate=tax_rate, file_path=file_path
    )

    if only_important:
        df = only_important_columns(df=df)
        df = set_columns_order(df=df)

    return df


"""
    df = pd.read_excel(io=file_path, sheet_name=sheet_name)
    df = clean_columns_names(df=df)
    df = drop_na_columns(df=df)
    df = merge_territorial_code(df=df)

    if only_important:
        df = only_important_columns(df=df)

    if JST_type is None:
        df = set_JST_type(df=df, file_path=file_path)

    df = normalize_JST_names(df=df)
    df = set_and_apply_tax_rate(
        df=df, year=year, tax_rate=tax_rate, file_path=file_path
    )

    # if df.attrs["JST_type"] == "NPP":
    #     df = sum_NPP_income(df=df)

    df = set_columns_order(df=df)
    return df
"""
