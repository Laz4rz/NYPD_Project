"""
this is __init__ file of the io_package
"""

from .load_incomes import load_income_excel
from .save import save_to_excel
from .load_population import load_population_excel

__all__ = ("load_income_excel", "save_to_excel", "load_population_excel")
