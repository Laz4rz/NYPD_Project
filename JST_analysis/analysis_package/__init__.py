"""
this is __init__ file of the analysis package
"""

from .incomes_comparison import compare_incomes
from .population_operations import (
    population_income_merge,
    calculate_JST,
    calculate_tax_mean,
)

__all__ = (
    "compare_incomes",
    "population_income_merge",
    "calculate_JST",
    "calculate_tax_mean",
)
