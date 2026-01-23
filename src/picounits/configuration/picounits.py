"""
Filename: picounits.py
Author: William Bowley
Version: 0.1
"""

DEFAULT_CONFIG = """
# picounits project configuration
# Drop this file in your project root (or any parent folder)
# picounits will automatically detect and use it
# Edit symbols and order to match your preferred notation

[symbols]
# Common analytical/natural units style (t = time, l = length, m = mass)
# Uncomment and modify as needed
# time: t
# length: l
# mass: m
# current: I
# TEMPERATURE: Θ
# amount: N
# luminosity: J
# dimensionless: 1

# Standard SI defaults (used if lines above are commented)
time: s
length: m
mass: kg
current: A
TEMPERATURE: K
amount: mol
luminosity: cd
dimensionless: ∅

[order]
# Change the order of dimensions in printed units
# Lower number = appears earlier (e.g., mass first in SI)
# Example for t/l/m style: time first
# TIME: 0
# LENGTH: 1
# MASS: 2

# Default SI order (mass · length · time · ...)
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
    "TEMPERATURE":          4,
    "AMOUNT":           5,
    "LUMINOSITY":       6,
    "DIMENSIONLESS":    7,
}

# Dimension maximum exponent size
MAX_EXPONENT = 10
