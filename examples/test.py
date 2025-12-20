from picounits.constants import LENGTH, TIME, MASS, VELOCITY, ENERGY
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
initial = 10 * VELOCITY
acc = 2.5 * (LENGTH / TIME ** 2)
dis = 12e3 * LENGTH
projectile_mass = 12 * MASS

""" Computes output values + dimensions """
vel = suvat(initial, acc, dis)
ke = kinetic_energy(projectile_mass, vel)

""" Prints output """
print(round(vel, 5), round(ke, 5))
