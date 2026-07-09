"""
Filename: constants.py

Description:
    Defines semantic physical quantities and their
    dimensional relationships in picounits.
"""

from picounits.core.unit import Unit
from picounits.core.dimensions import FBase, Dimension
from picounits.core.scales import PrefixScale


# =============== Predefined scales for quantities ===============


GIGA                    = PrefixScale.GIGA
giga                    = GIGA

MEGA                    = PrefixScale.MEGA
mega                    = MEGA

KILO                    = PrefixScale.KILO
kilo                    = KILO

CENTI                   = PrefixScale.CENTI
centi                   = CENTI

MILLI                   = PrefixScale.MILLI
milli                   = MILLI

MICRO                   = PrefixScale.MICRO
micro                   = MICRO

NANO                    = PrefixScale.NANO
nano                    = NANO

PICO                    = PrefixScale.PICO
pico                    = PICO


# =============== Fundamental dimensions ===============


TIME                    = Unit(Dimension(base=FBase.TIME))
time                    = TIME

LENGTH                  = Unit(Dimension(base=FBase.LENGTH))
length                  = LENGTH

MASS                    = Unit(Dimension(base=FBase.MASS))
mass                    = MASS

CURRENT                 = Unit(Dimension(base=FBase.CURRENT))
current                 = CURRENT

TEMPERATURE             = Unit(Dimension(base=FBase.TEMPERATURE))
temperature             = TEMPERATURE

AMOUNT                  = Unit(Dimension(base=FBase.AMOUNT))
amount                  = AMOUNT

LUMINOSITY              = Unit(Dimension(base=FBase.LUMINOSITY))
luminosity              = LUMINOSITY

DIMENSIONLESS           = Unit(Dimension(base=FBase.DIMENSIONLESS))
dimensionless           = DIMENSIONLESS

NULLSET                 = DIMENSIONLESS
nullset                 = NULLSET


# =============== Geometric quantities ===============


AREA                    = LENGTH ** 2
area                    = AREA

VOLUME                  = LENGTH ** 3
volume                  = VOLUME


# =============== Kinematics ===============


DISPLACEMENT            = LENGTH
displacement            = DISPLACEMENT

DISTANCE                = LENGTH
distance                = DISTANCE

VELOCITY                = LENGTH / TIME
velocity                = VELOCITY

SPEED                   = VELOCITY
speed                   = SPEED

ACCELERATION            = LENGTH / TIME ** 2
acceleration            = ACCELERATION

FREQUENCY               = DIMENSIONLESS / TIME
frequency               = FREQUENCY

PERIOD                  = TIME
period                  = PERIOD

WAVENUMBER              = DIMENSIONLESS / LENGTH
wavenumber              = WAVENUMBER

ANGULAR_FREQUENCY       = DIMENSIONLESS / TIME
angular_frequency       = ANGULAR_FREQUENCY

PHASE                   = DIMENSIONLESS
phase                   = PHASE


# =============== Classical mechanics ===============


FORCE                   = MASS * LENGTH / TIME ** 2
force                   = FORCE

MOMENTUM                = MASS * VELOCITY
momentum                = MOMENTUM

ANGULAR_MOMENTUM        = MASS * LENGTH ** 2 / TIME
angular_momentum        = ANGULAR_MOMENTUM

TORQUE                  = FORCE * LENGTH
torque                  = TORQUE

ENERGY                  = MASS * LENGTH ** 2 / TIME ** 2
energy                  = ENERGY

POWER                   = ENERGY / TIME
power                   = POWER

PRESSURE                = FORCE / AREA
pressure                = PRESSURE

DENSITY                 = MASS / VOLUME
density                 = DENSITY

WEIGHT                  = FORCE
weight                  = WEIGHT


# =============== Thermodynamics ===============


ENTROPY                     = ENERGY / TEMPERATURE
entropy                     = ENTROPY

HEAT_CAPACITY               = ENERGY / TEMPERATURE
heat_capacity               = HEAT_CAPACITY

SPECIFIC_HEAT               = ENERGY / (MASS * TEMPERATURE)
specific_heat               = SPECIFIC_HEAT

THERMAL_CONDUCTIVITY        = POWER / (LENGTH * TEMPERATURE)
thermal_conductivity        = THERMAL_CONDUCTIVITY

CONVECTION_COEFFICIENT      = POWER / (LENGTH**2 * TEMPERATURE)
convection_coefficient      = CONVECTION_COEFFICIENT

VOLUMETRIC_HEAT_CAPACITY    = HEAT_CAPACITY / VOLUME
volumetric_heat_capacity    = VOLUMETRIC_HEAT_CAPACITY

VOLUMETRIC_HEATING          = POWER / LENGTH ** 3
volumetric_heating          = VOLUMETRIC_HEATING

DIFFUSIVITY                 = LENGTH**2 * TIME**-1
diffusivity                 = DIFFUSIVITY


# =============== Electromagnetism ===============


CHARGE                  = CURRENT * TIME
charge                  = CHARGE

ELECTRIC_FIELD          = FORCE / CHARGE
electric_field          = ELECTRIC_FIELD

ELECTRIC_POTENTIAL      = ENERGY / CHARGE
electric_potential      = ELECTRIC_POTENTIAL

VOLTAGE                 = ELECTRIC_POTENTIAL
voltage                 = VOLTAGE

RESISTANCE              = VOLTAGE / CURRENT
resistance              = RESISTANCE

CONDUCTANCE             = DIMENSIONLESS / RESISTANCE
conductance             = CONDUCTANCE

CAPACITANCE             = CHARGE / VOLTAGE
capacitance             = CAPACITANCE

IMPEDANCE               = ENERGY / (TIME * CURRENT ** 2)
impedance               = IMPEDANCE

INDUCTANCE              = IMPEDANCE * TIME
inductance              = INDUCTANCE

MAGNETIC_FIELD          = FORCE / (CURRENT * LENGTH)
magnetic_field          = MAGNETIC_FIELD

MAGNETIC_FLUX           = MAGNETIC_FIELD * AREA
magnetic_flux           = MAGNETIC_FLUX

PERMEABILITY            = INDUCTANCE / LENGTH
permeability            = PERMEABILITY

FLUX_DENSITY            = MASS / (TIME ** 2 * CURRENT)
flux_density            = FLUX_DENSITY

COERCIVITY              = CURRENT / LENGTH
coercivity              = COERCIVITY

CONDUCTIVITY            = MASS ** -1 * LENGTH ** -3 * TIME ** 3 * CURRENT ** 2
conductivity            = CONDUCTIVITY


# =============== Waves & radiation ===============


INTENSITY               = POWER / AREA
intensity               = INTENSITY

LUMINANCE               = LUMINOSITY / AREA
luminance               = LUMINANCE

RADIANT_FLUX            = POWER
radiant_flux            = RADIANT_FLUX


# =============== Dimensionless semantic quantities ===============


STRAIN                  = DIMENSIONLESS
strain                  = STRAIN

REFRACTIVE_INDEX        = DIMENSIONLESS
refractive_index        = REFRACTIVE_INDEX

EFFICIENCY              = DIMENSIONLESS
efficiency              = EFFICIENCY

COEFFICIENT             = DIMENSIONLESS
coefficient             = COEFFICIENT

PROBABILITY             = DIMENSIONLESS
probability             = PROBABILITY
