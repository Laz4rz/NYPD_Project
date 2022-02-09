"""
This module lets you load an excel file in an expected population format
"""
import pandas as pd

from typing import Dict


def normalize_sheets_names():
    pass


def create_population_dict(excel_file: pd.ExcelFile) -> Dict:
    sheets_names = excel_file.sheet_names
    population_dict = {}
    for sheet_name in sheets_names:
        population_dict[sheet_name.lower()] = excel_file.parse(sheet_name)
    return population_dict


def load_population_excel(
    file_path: str,
    sheet_name: str = 0,
) -> Dict:
    excel_file = pd.ExcelFile(path_or_buffer=file_path)
    population_dict = create_population_dict(excel_file=excel_file)
    return population_dict
