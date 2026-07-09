# pylint: skip-file
# picounits\configuration\picounits.py

DEFAULT_CONFIG = """
# ==============================================================
# PicoUnits project configuration
#
# Drop this file in your project root (or any parent folder)
# PicoUnits will automatically detect and use it.
# Edit symbols and order to match your preferred notation
# ==============================================================

[symbols]
# Change the name of fundamental dimensions
time: s
length: m
mass: kg
current: A
TEMPERATURE: K
amount: mol
luminosity: cd
dimensionless: ∅

[order]
# Change the order of dimensions
MASS: 0
LENGTH: 1
TIME: 2
CURRENT: 3
TEMPERATURE: 4
AMOUNT: 5
LUMINOSITY: 6
DIMENSIONLESS: 7
""".lstrip()


# Package defaults symbols and order (SI)
DEFAULT_SYMBOLS = {
    "TIME":                 "s",
    "LENGTH":               "m",
    "MASS":                 "kg",
    "CURRENT":              "A",
    "TEMPERATURE":          "K",
    "AMOUNT":               "mol",
    "LUMINOSITY":           "cd",
    "DIMENSIONLESS":        "∅",
}


DEFAULT_ORDER = {
    "MASS":             0,
    "LENGTH":           1,
    "TIME":             2,
    "CURRENT":          3,
    "TEMPERATURE":      4,
    "AMOUNT":           5,
    "LUMINOSITY":       6,
    "DIMENSIONLESS":    7,
}


# Dimension maximum exponent size
MAX_EXPONENT = 10
DEFAULT_SIGNIFICANT_FIGURES = 3
