import pandas as pd


def check_integrity(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    integrity_columns = ["Kod", df1.attrs["JST_type"]]
    integrity_report = df1[integrity_columns].compare(df2[integrity_columns])
    if not integrity_report.empty:
        integrity_report = integrity_report.rename(
            columns={
                "self": df1.attrs['year'],
                "other": df2.attrs['year']
            }
        )
        print(
            f"Found {len(integrity_report)} integrity problems - they were skipped, check them by calling .attrs["
            f'"integrity_report"] on '
            f"the dataframe created with compare_incomes() function"
        )
    return integrity_report
