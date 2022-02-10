import unittest
import pandas as pd


class TestPopulation(unittest.TestCase):
    def test_create_population_dict(self):
        from JST_analysis.io_package.load_population import (
            create_population_dict,
            load_excel_pop,
        )

        excel_file = "../data/tabela12.xls"
        result = create_population_dict(load_excel_pop(excel_file))
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result.keys()), 16)

    def test_clean_dataframes(self):
        from JST_analysis.io_package.load_population import clean_columns_names

        df = pd.DataFrame({"xd": [None, None, "Dochody", None, None, None, 10]})
        df = clean_columns_names(df)
        self.assertListEqual(list(df.columns), ["index", "Dochody"])

    def test_aggregate_populations(self):
        from JST_analysis.io_package.load_population import (
            load_excel_pop,
            create_population_dict,
            clean_dataframes,
            aggregate_populations,
        )

        file_path = "../data/tabela12.xls"
        excel_file = load_excel_pop(file_path=file_path)
        population_dict = create_population_dict(excel_file=excel_file)
        population_dict = clean_dataframes(population_dict=population_dict)
        aggregated_population = aggregate_populations(population_dict=population_dict)
        self.assertIsInstance(aggregated_population, pd.DataFrame)
        self.assertEqual(len(aggregated_population.columns), 4)
