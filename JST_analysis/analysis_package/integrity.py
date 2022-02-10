import pandas as pd


def check_integrity(df1: pd.DataFrame, df2: pd.DataFrame, mode: str) -> pd.DataFrame:
    if mode == "merge":
        integrity_columns = ["Kod", df1.attrs["JST_type"], "województwo"]
        integrity_report = df1.merge(
            df2.drop_duplicates(),
            on=integrity_columns,
            how="left",
            indicator=True,
        )
        integrity_report = integrity_report[integrity_report["_merge"] != "both"]
        print(
            f"{mode}: Found {len(integrity_report)} integrity problems - they were skipped, check them by calling "
            f".attrs['integrity_report'] on the dataframe created with population_income_merge() function"
        )
        return integrity_report
    elif mode == "compare_incomes":
        integrity_columns = ["Kod", df1.attrs["JST_type"]]
        integrity_report = df1[integrity_columns].compare(df2[integrity_columns])
        if not integrity_report.empty:
            integrity_report = integrity_report.rename(
                columns={"self": df1.attrs["year"], "other": df2.attrs["year"]}
            )
            print(
                f"{mode}: Found {len(integrity_report)} integrity problems - they were skipped, check them by calling "
                f".attrs['integrity_report'] on the dataframe created with compare_incomes() function"
            )
        return integrity_report
    elif mode == "estimates":
        integrity_report = df1[df1[0].isna()]
        if not integrity_report.empty:
            print(
                f"{mode}: Found {len(integrity_report)} integrity problems - they were skipped, check them by calling "
                f".attrs['integrity_report'] on the dataframe created with calculate_estimates() function"
            )
        return integrity_report
