import unittest
import pandas as pd

class TestIncomes(unittest.TestCase):
    def test_sum_NPP_income(self):
        from JST_analysis.io_package.load_incomes import sum_NPP_income
        df = pd.DataFrame({"Kod": [75621, 75621], 'Dochody PIT': [100, 1], "NPP": ['a', 'a']})
        df = sum_NPP_income(df)
        self.assertEqual(df.iloc[0, 2], 101)

    def test_get_year(self):
        from JST_analysis.io_package.load_incomes import get_year
        year = get_year(file_path="data/2019/20200214_Gminy_za_2019.xlsx")
        self.assertEqual(year, '2019')
