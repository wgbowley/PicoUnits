"""
Filename: constants.py
Author: William Bowley
Version: 0.1

Description:
    This file defines generic units
    within the library such as meter,
    second, ampere etc
"""

from picounits.core.unit import Unit
from picounits.core.enums import FBase, Dimension


DIMENSIONLESS = Unit(Dimension(base=FBase.DIMENSIONLESS))

METER = Unit(Dimension(base=FBase.METER))
SECOND = Unit(Dimension(base=FBase.SECOND))
GRAM = Unit(Dimension(base=FBase.GRAM))
AMPERE = Unit(Dimension(base=FBase.AMPERE))
