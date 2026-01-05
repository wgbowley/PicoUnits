"""
Filename: basic.py
Author: William Bowley
Version: 0.1

Description:
    SUVAT and kinetic energy script showing
    dimensional correctness via picounits
"""

from picounits.constants import LENGTH, TIME, MASS, VELOCITY, ENERGY, KILO
from picounits.core.quantities.scalars.methods.validators import (
    unit_validator, Quantity as q
)

""" User variables """
Initial_Velocity = (10+100j) * VELOCITY
Acceleration = 2.5 * LENGTH / TIME ** 2
Displacement = (10+12j) * KILO * LENGTH
Projectile_Mass = 12 * MASS


@unit_validator(VELOCITY)
def suvat(initial_velocity: q, acceleration: q, distance: q) -> q:
    """ Calculates the velocity due to acceleration """
    square = initial_velocity ** 2 + 2 * acceleration * distance
    return square ** 0.5


@unit_validator(ENERGY)
def kinetic_energy(mass: q, velocity: q) -> q:
    """ Calculates the kinetic energy due to new velocity """
    return 0.5 * mass * velocity ** 2


if __name__ == "__main__":
    final_velocity = suvat(Initial_Velocity, Acceleration, Displacement)
    kinetic = kinetic_energy(Projectile_Mass, final_velocity)
    print(f"{final_velocity:.3f}", f"{kinetic:.3f}")
