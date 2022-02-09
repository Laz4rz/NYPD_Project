"""
Module containing informations about the tax rates for different JSTs and a function to set correct one for calculations
in different modules.
"""

tax_rates_by_JST = {
    "Gminy": {"2019": 0.3934, "2020": 0.3934},
    "Województwa": {"2019": 0.0160, "2020": 0.0160},
    "NPP": {
        "2019": {"75621": 0.3934, "75622": 0.1025},
        "2020": {"75621": 0.3934, "75622": 0.1025},
    },
    "Powiaty": {"2019": 0.1025, "2020": 0.1025},
}


def get_tax_rate(year: str, JST_type: str, chapter: str = None) -> float:
    if isinstance(chapter, str):
        return tax_rates_by_JST[JST_type][year][chapter]
    return tax_rates_by_JST[JST_type][year]
