"""
Filename: equations.py
Author: William Bowley
Version: 0.1

Description:
    Equations for a analytical coil-gun model
    as an example, for the picounits library
"""

from math import pi, ceil

from picounits.core.quantities import Quantity as q
from picounits.constants import (
    CURRENT, VOLTAGE, FLUX_DENSITY, FORCE, TIME, MASS, 
    INDUCTANCE, IMPEDANCE, MAGNETIC_PERMEABILITY, DIMENSIONLESS
)

@q.check(MASS)
def projectile_mass(axial_length: q, radius: q, density: q) -> q:
    """ Calculates the mass of the projectile """
    volume = pi * radius ** 2 * axial_length
    return volume * density

@q.check(DIMENSIONLESS)
def estimate_turns(
    axial_length: q, inner_radius: q, outer_radius: q, 
    wire_diameter: q, fill_factor: q
) -> q:
    """ Estimates the number of turns that can fit in a rectangular coil """
    slot_area = axial_length * (outer_radius - inner_radius)
    wire_area = wire_diameter ** 2
    effective_area = slot_area * fill_factor

    turns = effective_area / wire_area
    return ceil(turns)

@q.check(IMPEDANCE)
def cal_resistance(
    turns: q, mean_radius: q, wire_diameter: q, resistivity: q
) -> q:
    """ Calculates the resistance of the inductor """
    length = turns * pi * mean_radius
    area = pi * (wire_diameter / 2) ** 2
    return resistivity * length / area

@q.check(INDUCTANCE)
def cal_inductance(turns: q, axial_length: q, mean_radius: q) -> q:
    """ Calculates the inductance of solenoid """
    # Defines the permeability of free space
    permeability = 4 * pi * 1e-7 * MAGNETIC_PERMEABILITY

    area = pi * mean_radius ** 2
    return (turns ** 2 * area * permeability) / axial_length

@q.check(FORCE)
def projectile_drag(velocity: q, density: q, coefficient: q, radius: q) -> q:
    """ Calculates the drag force on the projectile """
    area = pi * radius ** 2
    velocity = velocity * abs(velocity)
    drag_force = -0.5 * density * velocity * area * coefficient
    return drag_force

@q.check(CURRENT / TIME)
def differential_currents(voltage: q, inductance: q) -> q:
    """ Differential equation for current within the system """
    return voltage / inductance

@q.check(CURRENT)
def clipping_current(current_limit: q, current: q) -> q:
    """ Limits the current to simulate a current limiting supply"""
    return min(current_limit, current)

@q.check(VOLTAGE)
def inductor_voltage(
    supply_voltage: q, current: q, resistance: q, induced_voltage: q
) -> q:
    """ Computes the inductor voltage during simulation"""
    voltage_drop = current * resistance
    return supply_voltage - voltage_drop + induced_voltage

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
    coil_radius: q, permeability: q, saturation: q
) -> q:
    """ Calculates the axial B-field inside a solenoid based on projectile position """
    b_constant = 0.5 * permeability * turns * current

    denom1 = (position ** 2 + coil_radius ** 2) ** 0.5
    term1 = position / denom1

    delta = position - coil_length
    denom2 = (delta ** 2 + coil_radius ** 2) ** 0.5
    term2 = delta / denom2

    b_field = b_constant * (term1 - term2)

    # Simple switch to mimic B-H curve
    if abs(b_field) > saturation:
        return saturation * (b_field / abs(b_field))

    return b_field

@q.check(FORCE)
def inst_force(
    b_field: q, permeability: q, projectile_outer_radius: q, direction: q
) -> q:
    """
    Calculate instantaneous force on a ferromagnetic projectile.

    Based on energy density in a magnetic field:
    F ≈ (1/2) * (B^2 / µ) * A, where A is the cross-sectional area.
    """
    cross_section = pi * projectile_outer_radius ** 2
    force_magnitude = 0.5 * (abs(b_field) * b_field / permeability) * cross_section

    return force_magnitude * direction
