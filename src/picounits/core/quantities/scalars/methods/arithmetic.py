"""
Filename: arithmetic.py
Author: William Bowley
Version: 0.2

Description:
    Defines the methods for arithmetic dunder
    and instance methods for scalar quantities
"""

from math import ceil

from picounits.core.unit import Unit
from picounits.constants import DIMENSIONLESS

from picounits.core.quantities.packet import Packet
from picounits.core.quantities.factory import Factory


def add_logic(q1: Packet, q2: Packet) -> Packet:
    """ Defines the logic for adding two packets """

    # Additions requires both packets to have the same Unit
    q1.unit_check(q2)

    # Calculates the new value and returns new packet
    new_value = q1.value + q2.value
    return Factory.create(new_value, q1.unit)


def sub_logic(q1: Packet, q2: Packet) -> Packet:
    """ Defines the logic for adding subtracting two packets """

    # Subtraction requires both packets to have the same Unit
    q1.unit_check(q2)

    # Calculates the new value and returns new packet
    new_value = q1.value - q2.value
    return Factory.create(new_value, q1.unit)


def multiplication_logic(q1: Packet, q2: Packet | Unit) -> Packet:
    """ Defines the logic for multiplication between two quantities"""

    if not isinstance(q2, Unit):
        # Calculates the new value and unit, then returns new packet
        new_value = q1.value * q2.value
        new_unit = q1.unit * q2.unit

        return Factory.create(new_value, new_unit)

    # Creates a syntactic bridge for defining quantities with units
    # Ex. 10 * Kilo = Q(10000, DIMENSIONLESS) -> Q * TIME -> Q(10000, s)
    if q1.unit == DIMENSIONLESS:
        return Factory.create(q1.value, q2)

    msg = f"Failed to perform multiplication between {q1} and {q2}"
    raise RuntimeError(msg)


def true_division_logic(q1: Packet, q2: Packet) -> Packet:
    """ Defines the logic for true division between two quantities """
    if q2.value == 0:
        m1, m2 = q1.value, q2.value  # inline length to long
        msg = f'True Division failed due to division by zero: {m1} / {m2}'
        raise ValueError(msg)

    # Calculates new value and unit, than returns packet
    new_value = q1.value / q2.value
    new_unit = q1.unit / q2.unit

    return Factory.create(new_value, new_unit)


def power_logic(q1: Packet, q2: Packet) -> Packet:
    """ Defines the logic for power between two quantities """
    if q2.unit != DIMENSIONLESS:
        msg = f"A unit cannot be raised to the power of a unit; {q1}^{q2}"
        raise TypeError(msg)

    # Handles zero exponent rule (x^0 = 1)
    if q2.value == 0:
        return Factory(1.0, DIMENSIONLESS)

    # Calculates new value and unit, than returns packet
    new_value = q1.value ** q2.value
    new_unit = q1.unit ** q2.value

    return Factory.create(new_value, new_unit)


def ceiling_logic(q1: Packet) -> Packet:
    """ Define the logic for ceiling of different types """
    value = q1.value
    if isinstance(value, complex):
        real_ceil = ceil(value.real)
        imag_ceil = ceil(value.imag)

        ceiling = complex(real_ceil, imag_ceil)
        return Factory.create(ceiling, q1.unit)

    if isinstance(value, (int, float)):
        return Factory.create(ceil(value), q1.unit)

    msg = f"{type(value)} isn't supported by {ceiling_logic.__name__}"
    raise TypeError(msg)


def square_root_logic(q: Packet) -> Packet:
    """ Defines the logic for the square root of a Quantity """
    return q ** (1 / 2)


def cubic_root_logic(q: Packet) -> Packet:
    """ Defines the logic for the cubic root of a Quantity """
    return q ** (1 / 3)
