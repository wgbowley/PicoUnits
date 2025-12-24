"""
Filename: equations.py
Author: William Bowley
Version: 0.1

Description:
    Equations for a analytical coil-gun model
    as an example, for the picounits library
"""

from math import pi

from picounits.core.qualities import Quantity as q
from picounits.constants import CURRENT, VOLTAGE, FLUX_DENSITY, FORCE, TIME

@q.check(CURRENT / TIME)
def differential_currents(voltage: q, inductance: q) -> q:
    """ Differential equation for current within the system """
    return voltage / inductance

@q.check(CURRENT)
def clipping_current(current_limit: q, current: q) -> q:
    """ Limits the current to simulate a current limiting supply"""
    return min(current_limit, current)

@q.check(VOLTAGE)
def inductor_voltage(supply_voltage: q, current: q, resistance: q) -> q:
    """ Computes the inductor voltage during simulation"""
    voltage_drop = current * resistance
    return supply_voltage - voltage_drop

@q.check(CURRENT)
def rk_2nd_order_current(
    current: q, voltage: q, inductance: q, resistance: q, step_size: q
) -> q:
    """ Solves the differential equation using Ralston's method"""
    k1 = differential_currents(voltage, inductance)

    # Updates the voltage for the next predicted frame
    voltage = voltage - resistance * 3 / 4 * step_size * k1
    k2 = differential_currents(voltage, inductance)

    current += (1 / 3 * k1 + 2 /3 * k2) * step_size
    return current

@q.check(FLUX_DENSITY)
def position_b_field(
    position: q, current: q, turns: q, coil_length: q, 
    coil_radius: q, permeability: q
) -> q:
    """ Calculates the axial B-field inside a solenoid based on projectile position """
    b_constant = 0.5 * permeability * turns * current

    denom1 = (position ** 2 + coil_radius ** 2) ** 0.5
    term1 = position / denom1

    delta = position - coil_length
    denom2 = (delta ** 2 + coil_radius ** 2) ** 0.5
    term2 = delta / denom2

    return b_constant * (term1 - term2)

@q.check(FORCE)
def inst_force(
    b_field: q, permeability: q, projectile_outer_radius: q,
    force_direction: int = 1 # +1 for forward, -1 for backward
) -> q:
    """
    Calculate instantaneous force on a ferromagnetic projectile.

    Based on energy density in a magnetic field:
    F ≈ (1/2) * (B^2 / µ) * A, where A is the cross-sectional area.
    """
    cross_section = pi * projectile_outer_radius ** 2
    force_magnitude = 0.5 * (b_field**2 / permeability) * cross_section

    return force_magnitude * force_direction
