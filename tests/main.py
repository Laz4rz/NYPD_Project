def test_income_comparison_routine():
    dict_2019 = {}
    path19 = r"../data/2019"

    dict_2020 = {}
    path = r"../data/2020"
    report_path = r"../data/reports"

    for enum, file in enumerate(os.listdir(path19)):
        dict_2019[enum] = load_income_excel(f"{path19}/{file}", only_important=True)

    for enum, file in enumerate(os.listdir(path)):
        dict_2020[enum] = load_income_excel(f"{path}/{file}", only_important=True)

    df = compare_incomes(dict_2019[0], dict_2020[2])
    save_to_excel(df, f"{report_path}/file_gmina.xlsx")

    df = compare_incomes(dict_2019[2], dict_2020[0])
    save_to_excel(df, f"{report_path}/file_powiat.xlsx")

    df = compare_incomes(dict_2019[3], dict_2020[1])
    save_to_excel(df, f"{report_path}/file_woje.xlsx")

    df = compare_incomes(dict_2019[1], dict_2020[3])
    save_to_excel(df, f"{report_path}/file_npp.xlsx")

    print("Income comparison routine passed without interruption")


def test_population_load_routine():
    path = r"C:\Users\szant\PycharmProjects\NYPD_Project\data\tabela12.xls"
    dict = load_population_excel(file_path=path)
    return dict


def test_both():
    dict_2020 = {}
    path = r"../data/2020"
    # report_path = r"../data/reports"

    for enum, file in enumerate(os.listdir(path)):
        dict_2020[enum] = load_income_excel(f"{path}/{file}", only_important=True)

    population_dict = test_population_load_routine()

    return dict_2020, population_dict


if __name__ == '__main__':
    import os
    import doctest

    from JST_analysis import (
        load_income_excel,
        save_to_excel,
        compare_incomes,
        load_population_excel,
        population_income_merge,
        calculate_JST,
        calculate_tax_mean,
        calculate_estimates,
    )

    doctest.testmod(verbose=True)
    income, population = test_both()
    df = population_income_merge(income[2], population)
    df1 = calculate_tax_mean(df=df)
    df2 = calculate_JST(df=df, JST_type="powiat")
    df3 = calculate_JST(df=df, JST_type="województwo")
    df4 = calculate_estimates(
        df_income_population=df, df_income=income[0], JST_level="powiat"
    )
    df5 = calculate_estimates(
        df_income_population=df, df_income=income[1], JST_level="województwo"
    )
