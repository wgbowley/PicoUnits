"""
Filename: transcendental.py
Author: William Bowley
Version: 0.3

Description:
    Defines the methods for transcendental mathematical
    functions methods for scalar quantities (REAL only)
"""

from math import (
    radians, degrees, sin, cos, tan, exp, log, log10, log2, e,
    asin, acos, atan, atan2, sinh, cosh, tanh, asinh, acosh, atanh
)

from picounits.core.unit import Unit
from picounits.core.quantities.packet import Packet
from picounits.core.quantities.factory import Factory


def _valid_input_for_transcendental(q: Packet, method: str) -> None:
    """ if unit is not dimensionless, it raises a value error """
    if q.unit == Unit.dimensionless():
        return None

    msg = (
        f"Method '{method}' requires dimensionless Quantity, "
        f"{q.unit} != {Unit.dimensionless()}"
    )
    raise ValueError(msg)


def _valid_input_for_inverse(q: Packet, method: str) -> None:
    """ If -1 > q.magnitude or q.magnitude > 1, raises a value error """
    if -1 <= q.magnitude <= 1:
        return

    m = q.magnitude
    msg = f"Method '{method}' requires input in range [-1, 1], got {m}"
    raise ValueError(msg)


def _valid_input_for_inverse_reciprocal(q: Packet, method: str) -> None:
    """ If |q.magnitude| < 1, raises a value error (for asec, acsc) """
    if abs(q.magnitude) >= 1:
        return

    m = q.magnitude
    msg = f"Method '{method}' requires |x| >= 1, got {m}"
    raise ValueError(msg)


def _valid_input_for_logarithms(
    q: Packet, n: float | int, method: str
) -> None:
    """ If q.magnitude <= 0 or n <= 0 or n == 1, raises value error """
    if not isinstance(n, (float, int)):
        mag = type(q.magnitude)
        msg = f"Method '{method}' requires a float or int, got {mag}"
        raise TypeError(msg)

    if q.magnitude <= 0:
        msg = f"Method '{method}' requires magnitude > 0, got {q.magnitude}"
        raise ValueError(msg)

    if n <= 0 or n == 1:
        msg = f"Method '{method}' requires "
        msg += "n != 1" if n == 1 else "n > 0"
        msg += f", got {n}"
        raise ValueError(msg)


""" ANGLE CONVERSION """


def to_radians_logic(q: Packet) -> Packet:
    """ Defines the logic for converting to radians with Quantities"""
    _valid_input_for_transcendental(q, to_radians_logic.__name__)
    new_magnitude = radians(q.magnitude)

    return Factory.create(new_magnitude, q.unit)


def to_degrees_logic(q: Packet) -> Packet:
    """ Defines the logic for converting to degrees with Quantities """
    _valid_input_for_transcendental(q, to_degrees_logic.__name__)
    new_magnitude = degrees(q.magnitude)

    return Factory.create(new_magnitude, q.unit)


""" BASIC TRIGONOMETRIC FUNCTIONS """


def sin_logic(q: Packet) -> Packet:
    """ Defines the logic for performing the sine operation on a Quantity """
    _valid_input_for_transcendental(q, sin_logic.__name__)
    new_magnitude = sin(q.magnitude)

    return Factory.create(new_magnitude, q.unit)


def cos_logic(q: Packet) -> Packet:
    """ Defines the logic for performing the cosine operation on a Quantity """
    _valid_input_for_transcendental(q, cos_logic.__name__)
    new_magnitude = cos(q.magnitude)

    return Factory.create(new_magnitude, q.unit)


def tan_logic(q: Packet) -> Packet:
    """
    Defines the logic for performing the tangent operation on a Quantity
    """
    _valid_input_for_transcendental(q, tan_logic.__name__)
    new_magnitude = tan(q.magnitude)

    return Factory.create(new_magnitude, q.unit)


def csc_logic(q: Packet) -> Packet:
    """
    Defines the logic for performing the cosecant operation on a Quantity
    """
    _valid_input_for_transcendental(q, csc_logic.__name__)
    new_magnitude = 1 / sin(q.magnitude)

    return Factory.create(new_magnitude, q.unit)


def sec_logic(q: Packet) -> Packet:
    """
    Defines the logic for performing the secant operation on a Quantity
    """
    _valid_input_for_transcendental(q, sec_logic.__name__)
    new_magnitude = 1 / cos(q.magnitude)

    return Factory.create(new_magnitude, q.unit)


def cot_logic(q: Packet) -> Packet:
    """
    Defines the logic for performing the cotangent operation on a Quantity
    """
    _valid_input_for_transcendental(q, cot_logic.__name__)
    new_magnitude = 1 / tan(q.magnitude)

    return Factory.create(new_magnitude, q.unit)


""" INVERSE TRIGONOMETRIC FUNCTIONS """


def asin_logic(q: Packet) -> Packet:
    """
    Defines the logic for performing the arc sine operation on a Quantity
    """
    _valid_input_for_transcendental(q, asin_logic.__name__)
    _valid_input_for_inverse(q, asin_logic.__name__)
    new_magnitude = asin(q.magnitude)

    return Factory.create(new_magnitude, q.unit)


def acos_logic(q: Packet) -> Packet:
    """
    Defines the logic for performing the arc cosine operation on a Quantity
    """
    _valid_input_for_transcendental(q, acos_logic.__name__)
    _valid_input_for_inverse(q, acos_logic.__name__)
    new_magnitude = acos(q.magnitude)

    return Factory.create(new_magnitude, q.unit)


def atan_logic(q: Packet) -> Packet:
    """
    Defines the logic for performing the arc tan operation on a Quantity
    """
    _valid_input_for_transcendental(q, atan_logic.__name__)
    new_magnitude = atan(q.magnitude)

    return Factory.create(new_magnitude, q.unit)


def atan2_logic(q_y: Packet, q_x: Packet) -> Packet:
    """
    Defines the logic for performing the arc tan 2 operation on a Quantity
    """
    # Ensures both q_y and q_x have the same unit
    q_y.unit_check(q_x)

    # Calculates the new magnitude, unit is always dimensionless
    new_magnitude = atan2(q_y.magnitude, q_x.magnitude)

    return Factory.create(new_magnitude, Unit.dimensionless())


def acsc_logic(q: Packet) -> Packet:
    """
    Defines the logic for performing the arc cosecant operation on a Quantity
    """
    _valid_input_for_transcendental(q, acsc_logic.__name__)
    _valid_input_for_inverse_reciprocal(q, acsc_logic.__name__)

    new_magnitude = asin(1 / q.magnitude)
    return Factory.create(new_magnitude, q.unit)


def asec_logic(q: Packet) -> Packet:
    """
    Defines the logic for performing the arc secant operation on a Quantity
    """
    _valid_input_for_transcendental(q, asec_logic.__name__)
    _valid_input_for_inverse_reciprocal(q, asec_logic.__name__)

    new_magnitude = acos(1 / q.magnitude)
    return Factory.create(new_magnitude, q.unit)


def acot_logic(q: Packet) -> Packet:
    """
    Defines the logic for performing the arc cotangent operation on a Quantity
    """
    _valid_input_for_transcendental(q, acot_logic.__name__)

    """
    Specific function check: If magnitude == 0, raises a ZeroDivisionError
    """
    if q.magnitude == 0:
        mag = q.magnitude
        msg = f"Method '{acot_logic.__name__}' requires q != 0, got {mag}"
        raise ZeroDivisionError(msg)

    new_magnitude = atan(1 / q.magnitude)

    return Factory.create(new_magnitude, q.unit)


""" HYPERBOLIC FUNCTIONS """


def sinh_logic(q: Packet) -> Packet:
    """ Defines the logic for performing the hyperbolic sine operation """
    _valid_input_for_transcendental(q, sinh_logic.__name__)
    new_magnitude = sinh(q.magnitude)

    return Factory.create(new_magnitude, q.unit)


def cosh_logic(q: Packet) -> Packet:
    """ Defines the logic for performing the hyperbolic cosine operation """
    _valid_input_for_transcendental(q, cosh_logic.__name__)
    new_magnitude = cosh(q.magnitude)

    return Factory.create(new_magnitude, q.unit)


def tanh_logic(q: Packet) -> Packet:
    """ Defines the logic for performing the hyperbolic tangent operation """
    _valid_input_for_transcendental(q, tanh_logic.__name__)
    new_magnitude = tanh(q.magnitude)

    return Factory.create(new_magnitude, q.unit)


def csch_logic(q: Packet) -> Packet:
    """ Defines the logic for performing the hyperbolic cosecant operation """
    _valid_input_for_transcendental(q, csch_logic.__name__)
    new_magnitude = 1 / sinh(q.magnitude)

    return Factory.create(new_magnitude, q.unit)


def sech_logic(q: Packet) -> Packet:
    """ Defines the logic for performing the hyperbolic secant operation """
    _valid_input_for_transcendental(q, sech_logic.__name__)
    new_magnitude = 1 / cosh(q.magnitude)

    return Factory.create(new_magnitude, q.unit)


def coth_logic(q: Packet) -> Packet:
    """ Defines the logic for performing the hyperbolic cotangent operation """
    _valid_input_for_transcendental(q, coth_logic.__name__)
    new_magnitude = 1 / tanh(q.magnitude)

    return Factory.create(new_magnitude, q.unit)


""" INVERSE HYPERBOLIC FUNCTIONS """


def asinh_logic(q: Packet) -> Packet:
    """
    Defines the logic for performing the inverse hyperbolic sine operation
    """
    _valid_input_for_transcendental(q, asinh_logic.__name__)
    new_magnitude = asinh(q.magnitude)

    return Factory.create(new_magnitude, q.unit)


def acosh_logic(q: Packet) -> Packet:
    """
    Defines the logic for performing the inverse hyperbolic cosine operation
    """
    _valid_input_for_transcendental(q, acosh_logic.__name__)

    """
    Specific function check: If magnitude < 1, raises a value error
    """
    if q.magnitude < 1:
        mag = q.magnitude
        msg = f"Method '{acosh_logic.__name__}' requires q >= 1, got {mag}"
        raise ValueError(msg)

    new_magnitude = acosh(q.magnitude)

    return Factory.create(new_magnitude, q.unit)


def atanh_logic(q: Packet) -> Packet:
    """
    Defines the logic for performing the inverse hyperbolic tangent operation
    """
    _valid_input_for_transcendental(q, atanh_logic.__name__)

    """
    Specific function check: If -1 >= magnitude or magnitude >= 1,
    raises a value error
    """
    if -1 >= q.magnitude or q.magnitude >= 1:
        mag = q.magnitude
        msg = f"Method '{atanh_logic.__name__}' requires -1 < q < 1, got {mag}"
        raise ValueError(msg)

    new_magnitude = atanh(q.magnitude)

    return Factory.create(new_magnitude, q.unit)


def acsch_logic(q: Packet) -> Packet:
    """
    Defines the logic for performing the inverse hyperbolic cosecant operation
    """
    _valid_input_for_transcendental(q, acsch_logic.__name__)

    """
    Specific function check: If magnitude equals 0, raises a value error
    """
    if q.magnitude == 0:
        mag = q.magnitude
        msg = f"Method '{acsch_logic.__name__}' requires q != 0, got {mag}"
        raise ValueError(msg)

    new_magnitude = asinh(1 / q.magnitude)
    return Factory.create(new_magnitude, q.unit)


def asech_logic(q: Packet) -> Packet:
    """
    Defines the logic for performing the inverse hyperbolic secant operation
    """
    _valid_input_for_transcendental(q, asech_logic.__name__)

    """
    Specific function check: If magnitude < 0 or magnitude > 1,
    raise a value error
    """
    if q.magnitude > 1 or q.magnitude <= 0:
        mag = q.magnitude
        msg = (
            f"Method '{asech_logic.__name__}' requires 0 < q <= 1, got {mag}"
        )
        raise ValueError(msg)

    new_magnitude = acosh(1 / q.magnitude)
    return Factory.create(new_magnitude, q.unit)


def acoth_logic(q: Packet) -> Packet:
    """
    Defines the logic for performing the inverse hyperbolic cotangent operation
    """
    _valid_input_for_transcendental(q, acoth_logic.__name__)

    """ Specific function check: If |magnitude| <= 1, raise value error """
    if abs(q.magnitude) <= 1:
        mag = q.magnitude
        msg = f"Method '{acoth_logic.__name__}' requires |q| > 1, got {mag}"
        raise ValueError(msg)

    new_magnitude = atanh(1 / q.magnitude)
    return Factory.create(new_magnitude, q.unit)


""" EXPONENTIAL AND LOGARITHMIC FUNCTIONS """


def exp_logic(q: Packet) -> Packet:
    """ Defines the logic for performing the exponential operation """
    _valid_input_for_transcendental(q, exp_logic.__name__)
    new_magnitude = exp(q.magnitude)

    return Factory.create(new_magnitude, q.unit)


def log_logic(q: Packet, n: float | int) -> Packet:
    """ Defines the logic for performing the variable log """
    _valid_input_for_transcendental(q, log_logic.__name__)
    _valid_input_for_logarithms(q, n, log_logic.__name__)

    new_magnitude = log(q.magnitude, n)
    return Factory.create(new_magnitude, q.unit)


def log2_logic(q: Packet) -> Packet:
    """ Defines the logic for performing the log 2 """
    _valid_input_for_transcendental(q, log2_logic.__name__)
    _valid_input_for_logarithms(q, 2, log2_logic.__name__)

    new_magnitude = log2(q.magnitude)
    return Factory.create(new_magnitude, q.unit)


def log10_logic(q: Packet) -> Packet:
    """ Defines the logic for performing the log 10 """
    _valid_input_for_transcendental(q, log10_logic.__name__)
    _valid_input_for_logarithms(q, 10, log10_logic.__name__)

    new_magnitude = log10(q.magnitude)
    return Factory.create(new_magnitude, q.unit)


def nlog_logic(q: Packet) -> Packet:
    """" Defines the logic for performing the natural logarithm """
    _valid_input_for_transcendental(q, nlog_logic.__name__)
    _valid_input_for_logarithms(q, e, nlog_logic.__name__)

    new_magnitude = log(q.magnitude)
    return Factory.create(new_magnitude, q.unit)
