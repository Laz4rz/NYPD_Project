"""
this is the __init__ file for the JST_analysis package
"""

from .io_package.load_incomes import load_income_excel
from .io_package.load_population import load_population_excel
from .io_package.save import save_to_excel
from .analysis_package.incomes_comparison import compare_incomes
from .analysis_package.population_operations import (
    population_income_merge,
    calculate_JST,
    calculate_tax_mean,
    calculate_estimates,
)

__all__ = (
    "load_income_excel",
    "compare_incomes",
    "save_to_excel",
    "load_population_excel",
    "population_income_merge",
    "calculate_JST",
    "calculate_tax_mean",
    "calculate_estimates",
)
