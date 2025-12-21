"""
Filename: analytical_motion.py
Author: William Bowley
Version: 0.1

Description:
    Example using picounits to ensure
    dimensional correctness in a simple
    suvat and kinetic energy problem  
"""

from picounits.constants import LENGTH, TIME, MASS, VELOCITY, ENERGY, MILLI, KILO
from picounits.core.qualities import Quantity as q


@q.check(VELOCITY)
def suvat(initial_velocity: q, acceleration: q, distance: q) -> q:
    """ Calculates the velocity due to acceleration """

    square = initial_velocity ** 2 + 2 * acceleration * distance
    return square ** 0.5

@q.check(ENERGY)
def kinetic_energy(mass: q, velocity: q) -> q:
    """ Calculates the kinetic energy due to new velocity """
    return 0.5 * mass * velocity ** 2

""" Input values """
initial = 10 * MILLI * VELOCITY
acc = 2.5 * (LENGTH / TIME ** 2)
dis = 12 * KILO * LENGTH
projectile_mass = 12 * MASS

""" Computes output values + dimensions """
vel = suvat(initial, acc, dis)
ke = kinetic_energy(projectile_mass, vel)

""" Prints output """
print(round(vel, 5), round(ke, 5))
