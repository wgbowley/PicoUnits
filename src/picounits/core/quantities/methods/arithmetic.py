"""
Filename: arithmetic.py
Author: William Bowley
Version: 0.2

Description:
    Defines the methods for arithmetic dunder and instance
    methods in Quantity via QuantityPacket

    NOTE: All these methods are logic methods
"""


from picounits.core.unit import Unit
from picounits.constants import DIMENSIONLESS

from picounits.core.quantities.packet import QuantityPacket


# Placeholder for the quantity packet type
ImplementedQ = type[QuantityPacket]


def add_logic(
    q1: QuantityPacket, q2: QuantityPacket, factory: ImplementedQ
) -> QuantityPacket:
    """ Defines the logic for adding two quantities """

    # Additions requires both packets to have the same Unit
    q1.unit_check(q2)

    # Calculates the new magnitude and returns new packet
    new_magnitude = q1.magnitude + q2.magnitude
    return factory(new_magnitude, q1.unit)


def sub_logic(
    q1: QuantityPacket, q2: QuantityPacket, factory: ImplementedQ
) -> QuantityPacket:
    """ Defines the logic for adding subtracting two quantities """

    # Subtraction requires both packets to have the same Unit
    q1.unit_check(q2)

    # Calculates the new magnitude and returns new packet
    new_magnitude = q1.magnitude - q2.magnitude
    return factory(new_magnitude, q1.unit)


def multiplication_logic(
    q1: QuantityPacket, q2: QuantityPacket | Unit, factory: ImplementedQ
) -> QuantityPacket:
    """ Defines the logic for multiplication between two quantities"""

    if not isinstance(q2, Unit):
        # Calculates the new magnitude and unit, then returns new packet
        new_value = q1.magnitude * q2.magnitude
        new_unit = q1.unit * q2.unit

        return factory(new_value, new_unit)

    # Creates a syntactic bridge for defining quantities with units
    # Ex. 10 * Kilo = Q(10000, DIMENSIONLESS) -> Q * TIME -> Q(10000, s)
    if q1.unit == DIMENSIONLESS:
        return factory(q1.magnitude, q2)

    msg = f"Failed to perform multiplication between {q1} and {q2}"
    raise RuntimeError(msg)


def true_division_logic(
    q1: QuantityPacket, q2: QuantityPacket, factory: ImplementedQ
) -> QuantityPacket:
    """ Defines the logic for true division between two quantities """
    if q2.magnitude == 0:
        m1, m2 = q1.magnitude, q2.magnitude  # inline length to long
        msg = f'True Division failed due to division by zero: {m1} / {m2}'
        raise ValueError(msg)

    # Calculates new magnitude and unit, than returns packet
    new_value = q1.magnitude / q2.magnitude
    new_unit = q1.unit / q2.unit

    return factory(new_value, new_unit)


def power_logic(
    q1: QuantityPacket, q2: QuantityPacket, factory: ImplementedQ
) -> QuantityPacket:
    """ Defines the logic for power between two quantities """
    if q2.unit != DIMENSIONLESS:
        msg = f"A unit cannot be raised to the power of a unit; {q1}^{q2}"
        raise TypeError(msg)

    # Handles zero exponent rule (x^0 = 1)
    if q2.magnitude == 0:
        return factory(1.0, DIMENSIONLESS)

    # Calculates new magnitude and unit, than returns packet
    new_value = q1.magnitude ** q2.magnitude
    new_unit = q1.unit ** q2.magnitude

    return factory(new_value, new_unit)
