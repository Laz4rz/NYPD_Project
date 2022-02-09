"""
this is __init__ file of the io_package
"""

from .load_incomes import load_excel
from .save import save_to_excel

__all__ = ("load_excel", "save_to_excel")
