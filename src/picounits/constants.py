"""
Filename: constants.py
Author: William Bowley
Version: 0.2

Description:
    Defines semantic physical quantities and their
    dimensional relationships in picounits.
"""

from picounits.core.unit import Unit
from picounits.core.dimensions import FBase, Dimension
from picounits.core.scales import PrefixScale

""" =============== Predefined scales for quantities =============== """

GIGA                    = PrefixScale.GIGA
MEGA                    = PrefixScale.MEGA
KILO                    = PrefixScale.KILO
CENTI                   = PrefixScale.CENTI
MILLI                   = PrefixScale.MILLI
MICRO                   = PrefixScale.MICRO
NANO                    = PrefixScale.NANO
PICO                    = PrefixScale.PICO


""" =============== Fundamental dimensions =============== """

TIME                    = Unit(Dimension(base=FBase.TIME))
LENGTH                  = Unit(Dimension(base=FBase.LENGTH))
MASS                    = Unit(Dimension(base=FBase.MASS))
CURRENT                 = Unit(Dimension(base=FBase.CURRENT))
TEMPERATURE             = Unit(Dimension(base=FBase.TEMPERATURE))
AMOUNT                  = Unit(Dimension(base=FBase.AMOUNT))
LUMINOSITY              = Unit(Dimension(base=FBase.LUMINOSITY))
DIMENSIONLESS           = Unit(Dimension(base=FBase.DIMENSIONLESS))


""" =============== Geometric quantities =============== """

AREA                    = LENGTH ** 2
VOLUME                  = LENGTH ** 3


""" =============== Kinematics =============== """

DISPLACEMENT            = LENGTH
DISTANCE                = LENGTH
VELOCITY                = LENGTH / TIME
SPEED                   = VELOCITY
ACCELERATION            = LENGTH / TIME ** 2
FREQUENCY               = DIMENSIONLESS / TIME
PERIOD                  = TIME
WAVENUMBER              = DIMENSIONLESS / LENGTH
ANGULAR_FREQUENCY       = DIMENSIONLESS / TIME
PHASE                   = DIMENSIONLESS


""" =============== Classical mechanics =============== """

FORCE                   = MASS * LENGTH / TIME ** 2
MOMENTUM                = MASS * VELOCITY
ANGULAR_MOMENTUM        = MASS * LENGTH ** 2 / TIME
TORQUE                  = FORCE * LENGTH
ENERGY                  = MASS * LENGTH ** 2 / TIME ** 2
POWER                   = ENERGY / TIME
PRESSURE                = FORCE / AREA
DENSITY                 = MASS / VOLUME
WEIGHT                  = FORCE


""" =============== Thermodynamics =============== """

ENTROPY                 = ENERGY / TEMPERATURE
HEAT_CAPACITY           = ENERGY / TEMPERATURE
SPECIFIC_HEAT           = ENERGY / (MASS * TEMPERATURE)
THERMAL_CONDUCTIVITY    = POWER / (LENGTH * TEMPERATURE)


""" =============== Electromagnetism =============== """

CHARGE                  = CURRENT * TIME
ELECTRIC_FIELD          = FORCE / CHARGE
ELECTRIC_POTENTIAL      = ENERGY / CHARGE
VOLTAGE                 = ELECTRIC_POTENTIAL
RESISTANCE              = VOLTAGE / CURRENT
CONDUCTANCE             = DIMENSIONLESS / RESISTANCE
CAPACITANCE             = CHARGE / VOLTAGE
IMPEDANCE               = ENERGY / (TIME * CURRENT ** 2)
INDUCTANCE              = IMPEDANCE * TIME
MAGNETIC_FIELD          = FORCE / (CURRENT * LENGTH)
MAGNETIC_FLUX           = MAGNETIC_FIELD * AREA
PERMEABILITY            = INDUCTANCE / LENGTH
FLUX_DENSITY            = MASS / (TIME ** 2 * CURRENT)
COERCIVITY              = CURRENT / LENGTH
CONDUCTIVITY            = MASS ** -1 * LENGTH ** -3 * TIME ** 3 * CURRENT ** 2


""" =============== Waves & radiation =============== """

INTENSITY               = POWER / AREA
LUMINANCE               = LUMINOSITY / AREA
RADIANT_FLUX            = POWER


""" =============== Dimensionless semantic quantities =============== """

STRAIN                  = DIMENSIONLESS
REFRACTIVE_INDEX        = DIMENSIONLESS
EFFICIENCY              = DIMENSIONLESS
COEFFICIENT             = DIMENSIONLESS
PROBABILITY             = DIMENSIONLESS
