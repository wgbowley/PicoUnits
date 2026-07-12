# pylint: skip-file
"""
Filename: Introduction.py

Descriptions:
    Introduces the mechanics of picounits via a few examples

    NOTE: Assumes your base dimensions are SI metric for (notation)
"""

def next_step(title):
    """ Helper functions for examples (Doesn't relate to library) """
    print(f"\n{'='*10} {title} {'='*10}")
    input(">>> Press Enter to see this example...")

""" ============ Set a value:unit pair ============ """

next_step("0: How to set a value:unit pair")

# Import the dimension & prefix you want to use
from picounits import LENGTH, MILLI


# Define a value:unit pair as (value, prefix, length)
william_height_m = 1.75 * LENGTH
william_height_mm = 1750 * MILLI * LENGTH

print(f"William (defined as m):  {william_height_m}")
print(f"William (defined as mm): {william_height_mm}")
print("Result: Picounits normalized both to 1.75 meters.")

" ============ Math Operations with value:units ============ "
next_step("1: Math Operations with value:units")

# Import the dimension & prefix you want to use
from picounits import MASS, FORCE, KILO


tommy_mass = 60 * MASS
car_mass = 1.5 * KILO * MASS

force_on_tommy = 100 * FORCE
force_on_car = -force_on_tommy

tommy_acceleration = force_on_tommy / tommy_mass
car_acceleration = force_on_car / car_mass

print(f"Tommy Acceleration: {tommy_acceleration:.3f}")
print(f"Car Acceleration:   {car_acceleration:.3f}")

" ============ Validation functions ============ "
next_step("2: Validates the output is the correct dimension")

# Import the quantity for type hinting, the validator for checking and dimensions to use
from picounits import Q, expects, CURRENT, VOLTAGE, RESISTANCE


@expects(RESISTANCE)
def calculate_voltage(current: Q, resistance: Q) -> Q:
    """ Calculates the voltage across an element based on v=ir (ohm's relation) """
    return current * resistance

try:
    print("Attempting calculate_voltage(10 A, 10 V)....")
    calculate_voltage(10 * CURRENT, 10 * VOLTAGE)

except Exception as err:
    print(f"`expects` catches dimension errors before they propagate: {err}")

print("Re-entry with calculate_voltage(10 A, 10 Ω)....")
print(f"Element voltage: {calculate_voltage(10 * CURRENT, 10 * RESISTANCE)}")

# ============ Example 3: Complex Numbers & SUVAT ============
next_step("3: Physics with Complex Numbers (SUVAT)")

from picounits import Q, expects, VELOCITY, TIME


@expects(VELOCITY)
def suvat(initial_velocity: Q, acceleration: Q, distance: Q) -> Q:
    """" Calculates the velocity after accelerating for a specific distance """
    square = initial_velocity ** 2 + 2 * acceleration * distance
    return square ** 0.5

# Variables with complex components
Initial_Velocity = (10+100j) * VELOCITY
Acceleration = 2.5 * LENGTH / TIME ** 2
Displacement = (10+12j) * KILO * LENGTH

final_v = suvat(Initial_Velocity, Acceleration, Displacement)
print(f"Complex Velocity Result: {final_v:.3f}")

# ============ Example 4: Scaling Collections ============
next_step("4: Scaling Lists/Arrays with Units")

from picounits import VOLTAGE, KILO, VOLTAGE


# You can scale a list of values directly by a unit
voltages = [1, 2, 3] * VOLTAGE
high_voltages = [10, 20, 30] * KILO * VOLTAGE

print(f"Standard Voltages: {voltages}")
print(f"High Voltages (kV scaled): {high_voltages}")

# ============ Example 5: Kinetic Energy ============
next_step("5: Derived Energy Calculation")

from picounits import Q, expects, ENERGY


@expects(ENERGY)
def kinetic_energy(mass: Q, velocity: Q) -> Q:
    """ Calculates the kinetic energy of the projectile """
    return 0.5 * mass * velocity ** 2

Projectile_Mass = 12 * MASS
energy = kinetic_energy(Projectile_Mass, final_v)
print(f"Final Kinetic Energy: {energy:.3f} J")

# # ============ Example 6: Parser (introduction.uiv) ============
# next_step("6: Parser (introduction.uiv)")


# from math import pi
# from pathlib import Path

# from picounits.extensions import Parser


# BASE_DIR = Path(__file__).parent
# library = BASE_DIR / "introduction.uiv"

# parameters = Parser.open(library)
# parameters.info("library")

# axial_length = parameters.pole.axial_length
# outer_radius = parameters.pole.outer_radius
# volume = pi * outer_radius ** 2 * axial_length

# print("Calculating pole volume using parameters")
# print(f"Pole Volume: {volume:.3f}")

# print("\n" + "="*30)
# print("Tutorial Complete!")
