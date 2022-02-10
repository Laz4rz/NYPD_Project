"""
This module lets you load an excel file in an expected population format
"""
import pandas as pd
from tqdm import tqdm

from typing import Dict


def create_population_dict(excel_file: pd.ExcelFile) -> Dict:
    print("Creating population dictionary...")
    sheets_names = excel_file.sheet_names
    population_dict = {}
    for sheet_name in sheets_names:
        population_dict[sheet_name.lower()] = excel_file.parse(sheet_name)
    return population_dict


def clean_dataframes(population_dict: Dict) -> Dict:
    print("Cleaning dataframes...")
    for key in population_dict.keys():
        population_dict[key] = clean_columns_names(df=population_dict[key])
        population_dict[key] = drop_unimportant(df=population_dict[key])
    return population_dict


def aggregate_populations(population_dict: Dict) -> pd.DataFrame:
    print("Aggregating populations...")
    df_aggr = pd.DataFrame(columns=(["Kod", "Gminy", "województwo", "Populacja"]))
    with tqdm(total=len(population_dict.keys())) as pbar:
        for key in population_dict.keys():
            pbar.update(1)
            df = population_dict[key]
            idx = 0
            while idx < len(df):
                if len(str(df.iloc[idx, 1]).strip(" ")) > 0:

                    start_idx = idx + 33
                    end_idx = idx + 48
                    population = df.iloc[start_idx:end_idx, 2].sum()
                    territorial_code = df.iloc[idx, 1]
                    gmina = df.iloc[idx, 0]

                    df_row = pd.DataFrame(
                        {
                            "Kod": territorial_code,
                            "Gminy": gmina.lower(),
                            "województwo": key,
                            "Populacja": population,
                        },
                        index=[0],
                    )
                    df_aggr = pd.concat([df_aggr, df_row], ignore_index=True)
                    idx += 71
                else:
                    idx += 1
    return df_aggr


def set_JST_type(df: pd.DataFrame) -> pd.DataFrame:
    df.attrs["JST_type"] = "Gminy"
    return df


def set_df_type(df: pd.DataFrame) -> pd.DataFrame:
    df.attrs["type"] = "populations"
    return df


def set_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    df = df.astype(
        {
            "Kod": "string",
            "Gminy": "string",
            "województwo": "string",
            "Populacja": "int32",
        }
    )
    return df


def clean_values(df: pd.DataFrame) -> pd.DataFrame:
    df = df.applymap(lambda x: x.lstrip() if isinstance(x, str) else x)
    df = df.applymap(lambda x: x.rstrip() if isinstance(x, str) else x)
    return df


def set_working_population(df: pd.DataFrame) -> pd.DataFrame:
    df["Populacja"] = df["Populacja"] * 0.9
    return df


def drop_unimportant(df: pd.DataFrame) -> pd.DataFrame:
    return df.iloc[:, 1:4]


def load_excel_pop(file_path: str) -> pd.ExcelFile:
    print("Loading Excel...")
    excel_file = pd.ExcelFile(path_or_buffer=file_path)
    return excel_file


def clean_columns_names(df: pd.DataFrame) -> pd.DataFrame:
    for column in df.columns:
        column_name = "".join(df[column][:6].dropna().tolist())
        df = df.rename(columns={column: column_name})
    df = df.iloc[7:]
    return df.reset_index()


def load_population_excel(
    file_path: str,
) -> pd.DataFrame:
    """
    This function lets you load an excel file containing data about the population for JSTs at Gmina level. You can
    operate on the data further with the population_operations module.
    :param file_path: path to the excel's file location
    :return: "populations" type dataframe
    """
    excel_file = load_excel_pop(file_path=file_path)
    population_dict = create_population_dict(excel_file=excel_file)
    population_dict = clean_dataframes(population_dict=population_dict)
    df = aggregate_populations(population_dict=population_dict)
    df = set_JST_type(df=df)
    df = set_df_type(df=df)
    df = set_dtypes(df=df)
    df = clean_values(df=df)
    df = set_working_population(df=df)
    return df
