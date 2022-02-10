import unittest
import pandas as pd


class TestIncomes(unittest.TestCase):
    def test_sum_NPP_income(self):
        from JST_analysis.io_package.load_incomes import sum_NPP_income
        df = pd.DataFrame({"Kod": [75621, 75621], 'Dochody PIT': [100, 1], "NPP": ['a', 'a']})
        df = sum_NPP_income(df)
        self.assertEqual(df.iloc[0, 2], 101)

    def test_sum_NPP_income_type(self):
        from JST_analysis.io_package.load_incomes import sum_NPP_income
        df = pd.DataFrame({"Kod": [75621, 75621], 'Dochody PIT': ['100', '1'], "NPP": ['a', 'a']})
        sum_NPP_income(df)
        self.assertRaises(TypeError)

    def test_get_year(self):
        from JST_analysis.io_package.load_incomes import get_year
        year = get_year(file_path="data/2019/20200214_Gminy_za_2019.xlsx")
        self.assertEqual(year, '2019')

    def test_clean_values(self):
        from JST_analysis.io_package.load_incomes import clean_values
        df = pd.DataFrame({"województwo": [" a aV  ", "aa V ", " aaaa a    ", 1]})
        df = clean_values(df)
        self.assertEqual(df.iloc[0, 0], 'a aV')

    def test_set_dtypes(self):
        import numpy as np
        from JST_analysis.io_package.load_incomes import set_dtypes
        df = pd.DataFrame(
            {"województwo": ["aaV", "aaV"], "Kod": [75621, 75622], 'Dochody PIT': [100, 1], "NPP": [100, 2],
             "powiat": [100, 100]})
        df.attrs['JST_type'] = "NPP"
        df = set_dtypes(df)
        self.assertTrue(isinstance(df.iloc[0, 0], str))
        self.assertTrue(isinstance(df.iloc[0, 1], str))
        self.assertTrue(isinstance(df.iloc[0, 2], np.float64))
        self.assertTrue(isinstance(df.iloc[0, 3], str))
        self.assertTrue(isinstance(df.iloc[0, 4], str))

    def test_set_df_type(self):
        from JST_analysis.io_package.load_incomes import set_df_type
        df = pd.DataFrame()
        df = set_df_type(df)
        self.assertEqual(df.attrs["type"], "income_base")

    def test_set_columns_order(self):
        from JST_analysis.io_package.load_incomes import set_columns_order
        df = pd.DataFrame({"województwo": ["aaV", "aaV"], "Kod": [75621, 75622], 'Dochody PIT': [100, 1], "NPP": [100, 2], "powiat": [100, 100]})
        df.attrs['JST_type'] = "NPP"
        columns_order = ["Kod", df.attrs["JST_type"], "województwo", "powiat", "Dochody PIT"]
        self.assertEqual(set_columns_order(df).columns.tolist(), columns_order)

    def test_only_important_columns(self):
        from JST_analysis.io_package.load_incomes import only_important_columns
        df = pd.DataFrame({"ROZDZIAŁ": [75621, 75622], 'Dochody PIT': [100, 1]})
        df.attrs['JST_type'] = "NPP"
        self.assertEqual(only_important_columns(df).columns.tolist(), ["Dochody PIT"])

    def test_set_and_apply_tax_rate(self):
        from JST_analysis.io_package.load_incomes import set_and_apply_tax_rate
        df = pd.DataFrame({"Gminy": ["aaV", "AAAAAA"], 'Dochody PIT': [100, 1]})
        df.attrs['JST_type'] = "Gminy"
        df = set_and_apply_tax_rate(df, "2020", None, None)
        self.assertEqual(df.loc[0, 'Dochody PIT'], "39.34")

        df = pd.DataFrame({"NPP": ["aaV", "aaV"], "ROZDZIAŁ": [75621, 75622], 'Dochody PIT': [100, 1]})
        df.attrs['JST_type'] = "NPP"
        df = set_and_apply_tax_rate(df, "2020", None, None)
        self.assertEqual(df.loc[0, 'Dochody PIT'], "39.44")

    def test_normalize_JST_names(self):
        from JST_analysis.io_package.load_incomes import normalize_JST_names
        df = pd.DataFrame({"Gminy": ["aaV", "AAAAAA"], 'xd': ["ABa", "BBC"]})
        df.attrs['JST_type'] = "Gminy"
        df = normalize_JST_names(df)
        self.assertEqual(df.loc[1, 'Gminy'], "aaaaaa")

    def test_set_JST_type(self):
        from JST_analysis.io_package.load_incomes import set_JST_type
        df = set_JST_type(pd.DataFrame({"WK": ["20", "30"], 'JST': ["20", "5"]}),
                     file_path="data/2019/20200214_Gminy_za_2019.xlsx")
        self.assertEqual(df.attrs['JST_type'], "Gminy")
        self.assertEqual(df.columns[1], "Gminy")

    def test_merge_territorial_code(self):
        from JST_analysis.io_package.load_incomes import merge_territorial_code
        df = merge_territorial_code(pd.DataFrame({"WK": ["20", "30"], "GK": ["1", '-'], 'xd': ["20", "5"]}))
        self.assertEqual(df.loc[0, "Kod"], "201")
        self.assertEqual(df.loc[1, "Kod"], "30")

    def test_drop_na_columns(self):
        from JST_analysis.io_package.load_incomes import drop_na_columns
        df = drop_na_columns(pd.DataFrame({"xd": [None, None, None, None, None, None, None]}))
        self.assertTrue(df.empty, True)

    def test_clean_column_names(self):
        from JST_analysis.io_package.load_incomes import clean_columns_names
        df = pd.DataFrame({"xd": [None, None, "Dochody", None, None, None, 10]})
        df = clean_columns_names(df)
        self.assertListEqual(list(df.columns), ['index', 'Dochody PIT'])
