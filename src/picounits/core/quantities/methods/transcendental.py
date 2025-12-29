"""
Filename: transcendental.py
Author: William Bowley
Version: 0.1

Description:
    Defines the methods for transcendental mathematical
    functions methods in Quantity via QuantityPacket

    NOTE: All these methods are logic methods
"""

from math import (
    radians, degrees, sin, cos, tan, exp, log, log10, log2, e,
    asin, acos, atan, atan2

)

from picounits.constants import DIMENSIONLESS
from picounits.core.quantities.packet import QuantityPacket


# Placeholder for the quantity packet type
ImplementedQ = type[QuantityPacket]


def _valid_input_for_transcendental(q: QuantityPacket, method: str) -> None:
    """ if unit is not dimensionless, it raises a value error """
    if q.unit is DIMENSIONLESS:
        return None

    msg = (
        f"Methods '{method}' requires non-dimensionless Quantity, "
        f"{q.unit} != {DIMENSIONLESS}"
    )
    raise ValueError(msg)


def _valid_input_for_inverse(q: QuantityPacket, method: str) -> None:
    """ If -1 > q.magnitude or q.magnitude > 1, than raises a value error """
    if -1 <= q.magnitude <= 1:
        return

    m = q.magnitude  # Inline length too long
    msg = f"Method '{method}' requires input in range [1, -1], got {m}"
    raise ValueError(msg)


def _valid_input_for_logarithms(
    q: QuantityPacket, n: int, method: str
) -> None:
    """ If q.magnitude < 0 or n <= 0 or n == 1, than raise value error """
    if q.magnitude <= 0:
        msg = f"Method '{method}'requires {q.magnitude} <= 0"
        raise ValueError(msg)

    if n <= 0 or n == 1:
        msg = f"Methods '{method} requires "

        # Logic for routing cause for the user message
        msg += "n==1" if n == 1 else "n <= 0"
        msg += f", got {n}"
        raise ValueError(msg)


def to_radians_logic(
    q: QuantityPacket, factory: ImplementedQ
) -> QuantityPacket:
    """ Defines the logic for converting to radians with Quantities"""
    _valid_input_for_transcendental(q, to_radians_logic.__name__)
    new_magnitude = radians(q.magnitude)

    return factory(new_magnitude, q.unit)


def to_degrees_logic(
    q: QuantityPacket, factory: ImplementedQ
) -> QuantityPacket:
    """ Defines the logic for converting to degrees with Quantities """
    _valid_input_for_transcendental(q, to_degrees_logic.__name__)
    new_magnitude = degrees(q.magnitude)

    return factory(new_magnitude, q.unit)


def sin_logic(q: QuantityPacket, factory: ImplementedQ) -> QuantityPacket:
    """ Defines the logic for performing the sine operation on a quantity """
    _valid_input_for_transcendental(q, sin_logic.__name__)
    new_magnitude = sin(q.magnitude)

    return factory(new_magnitude, q.unit)


def cos_logic(q: QuantityPacket, factory: ImplementedQ) -> QuantityPacket:
    """ Defines the logic for performing the cosine operation on a Quantity """
    _valid_input_for_transcendental(q, cos_logic.__name__)
    new_magnitude = cos(q.magnitude)

    return factory(new_magnitude, q.unit)


def tan_logic(q: QuantityPacket, factory: ImplementedQ) -> QuantityPacket:
    """ Defines the logic for performing the tan operation on a Quantity """
    _valid_input_for_transcendental(q, tan_logic.__name__)
    new_magnitude = tan(q.magnitude)

    return factory(new_magnitude, q.unit)


def exp_logic(q: QuantityPacket, factory: ImplementedQ) -> QuantityPacket:
    """ Defines the logic for performing the exponential operation """
    _valid_input_for_transcendental(q, exp_logic.__name__)
    new_magnitude = exp(q.magnitude)

    return factory(new_magnitude, q.unit)


def log_logic(
    q: QuantityPacket, n: float, factory: ImplementedQ
) -> QuantityPacket:
    """ Defines the logic for performing the variable log """
    _valid_input_for_transcendental(q, log_logic.__name__)
    _valid_input_for_logarithms(q, n, log_logic.__name__)

    new_magnitude = log(q.magnitude, n)
    return factory(new_magnitude, q.unit)


def log2_logic(q: QuantityPacket, factory: ImplementedQ) -> QuantityPacket:
    """ Defines the logic for performing the log 2 """
    _valid_input_for_transcendental(q, log2_logic.__name__)
    _valid_input_for_logarithms(q, 2, log2_logic.__name__)
    new_magnitude = log2(q.magnitude)

    return factory(new_magnitude, q.unit)


def log10_logic(q: QuantityPacket, factory: ImplementedQ) -> QuantityPacket:
    """ Defines the logic for performing the log 10 """
    _valid_input_for_transcendental(q, log10_logic.__name__)
    _valid_input_for_logarithms(q, 10, log10_logic.__name__)
    new_magnitude = log10(q.magnitude)

    return factory(new_magnitude, q.unit)


def nlog_logic(q: QuantityPacket, factory: ImplementedQ) -> QuantityPacket:
    """" Defines the logic for performing the natural logarithm """
    _valid_input_for_transcendental(q, nlog_logic.__name__)
    _valid_input_for_logarithms(q, e, log_logic.__name__)
    new_magnitude = log(q.magnitude)

    return factory(new_magnitude, q.unit)
