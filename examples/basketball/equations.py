"""
Filename: equations.py
Author: William Bowley
Version: 0.1

Description:
    Equations for analytical projectile model
    as an example, for the picounits library
"""

from math import pi

from picounits.core import unit_validator, Quantity as q
from picounits import LENGTH, MASS, FORCE


@unit_validator(MASS)
def projectile_mass(radius: q, density: q) -> q:
    """ Calculates the drag force on the ball """
    volume = 4 / 3 * pi * radius ** 3
    return volume * density


@unit_validator(LENGTH)
def calculate_displacement(origin: q, position: q) -> q:
    """ Calculates the displacement of the projectile """
    origin.unit_check(position)

    difference = position - origin
    return difference.magnitude * origin.unit


@unit_validator(FORCE)
def calculate_drag(velocity: q, density: q, coefficient: q, radius: q) -> q:
    """ Calculate the drag force on the ball """
    area = pi * radius ** 2

    def _single_axis_drag(v) -> float:
        """ Calculates the drag force on the ball for a single axis """
        v = v.value * abs(v.value)  # Retains directionally
        return - 0.5 * density * v * area * coefficient

    # Extracts velocity and calculates force
    vi, vj, vk = velocity
    return [
        _single_axis_drag(vi),
        _single_axis_drag(vj),
        _single_axis_drag(vk)
    ] * FORCE
