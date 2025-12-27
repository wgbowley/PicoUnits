"""
Filename: equations.py
Author: William Bowley
Version: 0.1

Description:
    Equations for analytical model for 
    3D projectile motion simulation
"""

from math import pi

from picounits.core.quantities import Quantity as q
from picounits.constants import MASS, FORCE, LENGTH

@q.check(FORCE)
def _single_axis_drag(velocity: q, density: q, coefficient: q, radius: q) -> q:
    """ Calculates the drag force on the ball for a single axis """
    area = pi * radius ** 2
    velocity = velocity * abs(velocity)
    drag_force = -0.5 * density * velocity * area * coefficient

    return drag_force

@q.check(MASS)
def ball_mass(radius: q, density: q) -> q:
    """ Calculates the mass of the ball """
    volume = 4 / 3 * pi * radius ** 3
    return volume * density

@q.check(FORCE)
def ball_drag(
    velocity: tuple[q, q, q], density: q, coefficient: q, radius: q
) -> tuple[q, q, q]:
    """ Calculates the drag force on the ball """
    vi, vj, vk = velocity

    # Calculates the drag force for each axis
    fi = _single_axis_drag(vi, density, coefficient, radius)
    fj = _single_axis_drag(vj, density, coefficient, radius)
    fk = _single_axis_drag(vk, density, coefficient, radius)

    return fi, fj, fk

@q.check(LENGTH)
def calculate_displacement(
    origin: tuple[q, q, q], position: tuple[q, q, q]
)-> q:
    """ Calculates the displacement of an object"""
    i2, j2, k2 = position
    i1, j1, k1 = origin

    # Calculates the magnitude of the difference i.e displacement
    radicand = (i2-i1) ** 2 + (j2-j1) ** 2 + (k2-k1) ** 2
    return radicand ** 0.5

@q.check(FORCE)
def force_vector(force: q, elevation: q, azimuth: q) -> tuple[q, q, q]:
    """ 
    Calculates the directional unit vectors and than resultant force vector
    """
    elev_rad = elevation.to_radians()
    az_rad = azimuth.to_radians()

    # Total horizontal force
    f_horizontal = force * elev_rad.cos()

    fi = f_horizontal * az_rad.sin()
    fj = f_horizontal * az_rad.cos()
    fk = force * elev_rad.sin()

    return fi, fj, fk
