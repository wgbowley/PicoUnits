"""
Filename: comparison.py
Author: William Bowley
Version: 0.2

Description:
    Defines the methods for comparison dunder and instance
    methods in Quantity via QuantityPacket

    NOTE: All these methods are logic methods
"""


from picounits.core.quantities.packet import QuantityPacket


def _valid_comparison(q1: QuantityPacket, q2: QuantityPacket) -> None:
    """
    Raises a ValueError if q1.unit != q2.unit, if not returns none

    NOTE: Does not use the in-build QuantityPacket.check_unit() to allow
    for more informative  error messages
    """
    if q1.unit == q2.unit:
        return

    msg = f"Cannot compare different units, {q1.unit} != {q2.unit}"
    raise ValueError(msg)


def less_than_comparison_logic(q1: QuantityPacket, q2: QuantityPacket) -> bool:
    """ Defines the behavior for less than comparison """
    _valid_comparison(q1, q2)
    return q1.magnitude < q2.magnitude


def less_than_or_equal_to_comparison_logic(
    q1: QuantityPacket, q2: QuantityPacket
) -> bool:
    """ Defines the behavior for less than or equal to comparison """
    _valid_comparison(q1, q2)
    return q1.magnitude <= q2.magnitude


def greater_than_comparison_logic(
    q1: QuantityPacket, q2: QuantityPacket
) -> bool:
    """ Defines the behavior for greater than comparison """
    _valid_comparison(q1, q2)
    return q1.magnitude > q2.magnitude


def greater_than_or_equal_comparison_logic(
    q1: QuantityPacket, q2: QuantityPacket
) -> bool:
    """ Defines the behavior for greater than or equal comparison """
    _valid_comparison(q1, q2)
    return q1.magnitude >= q2.magnitude


def equality_comparison_logic(q1: QuantityPacket, q2: QuantityPacket) -> bool:
    """ Defines the behavior for equality comparison """
    if q1.unit != q2.unit:
        # Unit equality matters
        return False

    return q1.magnitude == q2.magnitude
