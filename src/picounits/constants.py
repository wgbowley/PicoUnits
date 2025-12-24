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
from picounits.core.enums import FBase, Dimension, PrefixScale

""" Predefined scales for quantities """

GIGA = PrefixScale.GIGA
KILO = PrefixScale.KILO
CENTI = PrefixScale.CENTI
MILLI = PrefixScale.MILLI
NANO = PrefixScale.NANO

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

ACCELERATION = LENGTH / TIME ** 2
VELOCITY = LENGTH / TIME ** 1
POWER = MASS * LENGTH ** 2 / TIME ** 3
ENERGY = MASS * LENGTH ** 2 / TIME ** 2
FORCE = MASS * LENGTH / TIME ** 2
FLUX_DENSITY = MASS / (TIME ** 2 * CURRENT)
IMPEDANCE = ENERGY / (TIME * CURRENT ** 2)
INDUCTANCE = IMPEDANCE * TIME
MAGNETIC_PERMEABILITY = INDUCTANCE / LENGTH
VOLTAGE = POWER / CURRENT
