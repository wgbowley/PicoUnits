"""
Filename: arithmetic.py
Author: William Bowley
Version: 0.2

Description:
    Defines the methods for arithmetic dunder and instance
    methods in Quantity & CQuantity via VPacket
"""

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

    # Negative values to the power of a fraction returns a complex number
    if q1.value < 0 and q2.value < 1:
        """ This logic is incorrect """
        value = complex(q1.value)

        # Calculates new value and unit, than returns packet
        new_value = value ** q2.value
        new_unit = q1.unit ** q2.value
        return Factory.create(new_value, new_unit)

    # Calculates new value and unit, than returns packet
    new_value = q1.value ** q2.value
    new_unit = q1.unit ** q2.value

    return Factory.create(new_value, new_unit)


def square_root_logic(q: Packet) -> Packet:
    """ Defines the logic for the square root of a Quantity """
    return q ** (1 / 2)


def cubic_root_logic(q: Packet) -> Packet:
    """ Defines the logic for the cubic root of a Quantity """
    return q ** (1 / 3)
