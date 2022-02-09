from JST_analysis import load_excel, save_to_excel, compare_incomes
import os


def test_income_comparison_routine():
    dict_2019 = {}
    path19 = r"../data/2019"

    dict_2020 = {}
    path = r"../data/2020"
    report_path = r"../data/reports"

    for enum, file in enumerate(os.listdir(path19)):
        dict_2019[enum] = load_excel(f"{path19}/{file}", only_important=True)

    for enum, file in enumerate(os.listdir(path)):
        dict_2020[enum] = load_excel(f"{path}/{file}", only_important=True)

    df = compare_incomes(dict_2019[0], dict_2020[2])
    save_to_excel(df, f"{report_path}/file_gmina.xlsx")

    df = compare_incomes(dict_2019[2], dict_2020[0])
    save_to_excel(df, f"{report_path}/file_powiat.xlsx")

    df = compare_incomes(dict_2019[3], dict_2020[1])
    save_to_excel(df, f"{report_path}/file_woje.xlsx")

    df = compare_incomes(dict_2019[1], dict_2020[3])
    save_to_excel(df, f"{report_path}/file_npp.xlsx")

    print("Income comparison routine passed without interruption")
