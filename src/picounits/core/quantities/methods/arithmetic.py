"""
Filename: arithmetic.py
Author: William Bowley
Version: 0.2

Description:
    Defines the methods for arithmetic dunder and instance
    methods in Quantity & CQuantity via VPacket

    NOTE: All these methods are logic methods
"""

from picounits.core.unit import Unit
from picounits.constants import DIMENSIONLESS

from picounits.core.quantities.vpacket import VPacket


# Placeholder for the quantity packet type
ImplementedQ = type[VPacket]


def add_logic(
    q1: VPacket, q2: VPacket, factory: ImplementedQ
) -> VPacket:
    """ Defines the logic for adding two quantities """

    # Additions requires both packets to have the same Unit
    q1.unit_check(q2)

    # Calculates the new value and returns new packet
    new_value = q1.value + q2.value
    return factory(new_value, q1.unit)


def sub_logic(
    q1: VPacket, q2: VPacket, factory: ImplementedQ
) -> VPacket:
    """ Defines the logic for adding subtracting two quantities """

    # Subtraction requires both packets to have the same Unit
    q1.unit_check(q2)

    # Calculates the new value and returns new packet
    new_value = q1.value - q2.value
    return factory(new_value, q1.unit)


def multiplication_logic(
    q1: VPacket, q2: VPacket | Unit, factory: ImplementedQ
) -> VPacket:
    """ Defines the logic for multiplication between two quantities"""

    if not isinstance(q2, Unit):
        # Calculates the new value and unit, then returns new packet
        new_value = q1.value * q2.value
        new_unit = q1.unit * q2.unit

        return factory(new_value, new_unit)

    # Creates a syntactic bridge for defining quantities with units
    # Ex. 10 * Kilo = Q(10000, DIMENSIONLESS) -> Q * TIME -> Q(10000, s)
    if q1.unit == DIMENSIONLESS:
        return factory(q1.value, q2)

    msg = f"Failed to perform multiplication between {q1} and {q2}"
    raise RuntimeError(msg)


def true_division_logic(
    q1: VPacket, q2: VPacket, factory: ImplementedQ
) -> VPacket:
    """ Defines the logic for true division between two quantities """
    if q2.value == 0:
        m1, m2 = q1.value, q2.value  # inline length to long
        msg = f'True Division failed due to division by zero: {m1} / {m2}'
        raise ValueError(msg)

    # Calculates new value and unit, than returns packet
    new_value = q1.value / q2.value
    new_unit = q1.unit / q2.unit

    return factory(new_value, new_unit)


def power_logic(
    q1: VPacket, q2: VPacket, factory: ImplementedQ
) -> VPacket:
    """ Defines the logic for power between two quantities """
    if q2.unit != DIMENSIONLESS:
        msg = f"A unit cannot be raised to the power of a unit; {q1}^{q2}"
        raise TypeError(msg)

    # Handles zero exponent rule (x^0 = 1)
    if q2.value == 0:
        return factory(1.0, DIMENSIONLESS)

    # Calculates new value and unit, than returns packet
    new_value = q1.value ** q2.value
    new_unit = q1.unit ** q2.value

    return factory(new_value, new_unit)


def square_root_logic(q: VPacket) -> VPacket:
    """ Defines the logic for the square root of a Quantity """
    return q ** (1 / 2)


def cubic_root_logic(q: VPacket) -> VPacket:
    """ Defines the logic for the cubic root of a Quantity """
    return q ** (1 / 3)
