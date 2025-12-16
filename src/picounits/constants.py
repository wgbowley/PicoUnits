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
from picounits.core.enums import SIBase, Dimension


DIMENSIONLESS = Unit(Dimension(base=SIBase.DIMENSIONLESS))

METER = Unit(Dimension(base=SIBase.METER))
SECOND = Unit(Dimension(base=SIBase.SECOND))
GRAM = Unit(Dimension(base=SIBase.GRAM))
AMPERE = Unit(Dimension(base=SIBase.AMPERE))
