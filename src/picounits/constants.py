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


""" Predefined fundamental units"""

TIME = Unit(Dimension(base=FBase.TIME))
LENGTH = Unit(Dimension(base=FBase.LENGTH))
MASS = Unit(Dimension(base=FBase.MASS))
CURRENT = Unit(Dimension(base=FBase.CURRENT))
THERMAL = Unit(Dimension(base=FBase.THERMAL))
AMOUNT = Unit(Dimension(base=FBase.AMOUNT))
LUMINOSITY  = Unit(Dimension(base=FBase.LUMINOSITY))
DIMENSIONLESS = Unit(Dimension(base=FBase.DIMENSIONLESS))


""" Predefined units """

VELOCITY = LENGTH / TIME ** 1
FLUX = MASS * LENGTH ** 2 / TIME ** 3
EFFORT = MASS * LENGTH ** 2 / TIME ** 2
VIGOUR = MASS * LENGTH / TIME ** 2
FLEXION = MASS / (TIME ** 2 * CURRENT)
IMPEDANCE = EFFORT / (TIME * CURRENT ** 2)
