"""
Filename: transcendental.py
Author: William Bowley
Version: 0.2

Description:
    Defines the methods for transcendental mathematical
    functions methods in Quantity via VPacket

    NOTE: All these methods are logic methods
"""

from math import (
    radians, degrees, sin, cos, tan, exp, log, log10, log2, e,
    asin, acos, atan, atan2, sinh, cosh, tanh, asinh, acosh, atanh
)

from picounits.constants import DIMENSIONLESS
from picounits.core.quantities.vpacket import VPacket


# Placeholder for the quantity packet type
ImplementedQ = type[VPacket]


def _valid_input_for_transcendental(q: VPacket, method: str) -> None:
    """ if unit is not dimensionless, it raises a value error """
    if q.unit is DIMENSIONLESS:
        return None

    msg = (
        f"Method '{method}' requires dimensionless Quantity, "
        f"{q.unit} != {DIMENSIONLESS}"
    )
    raise ValueError(msg)


def _valid_input_for_inverse(q: VPacket, method: str) -> None:
    """ If -1 > q.value or q.value > 1, raises a value error """
    if -1 <= q.value <= 1:
        return

    m = q.value
    msg = f"Method '{method}' requires input in range [-1, 1], got {m}"
    raise ValueError(msg)


def _valid_input_for_inverse_reciprocal(
    q: VPacket, method: str
) -> None:
    """ If |q.value| < 1, raises a value error (for asec, acsc) """
    if abs(q.value) >= 1:
        return

    m = q.value
    msg = f"Method '{method}' requires |x| >= 1, got {m}"
    raise ValueError(msg)


def _valid_input_for_logarithms(
    q: VPacket, n: float | int, method: str
) -> None:
    """ If q.value <= 0 or n <= 0 or n == 1, raises value error """
    if not isinstance(n, (float, int)):
        mag = type(q.value)     # Inline length too long
        msg = f"Method '{method}' requires a float or int, got {mag}"
        raise TypeError(msg)

    if q.value <= 0:
        msg = f"Method '{method}' requires value > 0, got {q.value}"
        raise ValueError(msg)

    if n <= 0 or n == 1:
        msg = f"Method '{method}' requires "
        msg += "n != 1" if n == 1 else "n > 0"
        msg += f", got {n}"
        raise ValueError(msg)


""" ANGLE CONVERSION """


def to_radians_logic(
    q: VPacket, factory: ImplementedQ
) -> VPacket:
    """ Defines the logic for converting to radians with Quantities"""
    _valid_input_for_transcendental(q, to_radians_logic.__name__)
    new_value = radians(q.value)

    return factory(new_value, q.unit)


def to_degrees_logic(
    q: VPacket, factory: ImplementedQ
) -> VPacket:
    """ Defines the logic for converting to degrees with Quantities """
    _valid_input_for_transcendental(q, to_degrees_logic.__name__)
    new_value = degrees(q.value)

    return factory(new_value, q.unit)


""" BASIC TRIGONOMETRIC FUNCTIONS """


def sin_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """ Defines the logic for performing the sine operation on a Quantity """
    _valid_input_for_transcendental(q, sin_logic.__name__)
    new_value = sin(q.value)

    return factory(new_value, q.unit)


def cos_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """ Defines the logic for performing the cosine operation on a Quantity """
    _valid_input_for_transcendental(q, cos_logic.__name__)
    new_value = cos(q.value)

    return factory(new_value, q.unit)


def tan_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """
    Defines the logic for performing the tangent operation on a Quantity
    """
    _valid_input_for_transcendental(q, tan_logic.__name__)
    new_value = tan(q.value)

    return factory(new_value, q.unit)


def csc_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """
    Defines the logic for performing the cosecant operation on a Quantity
    """
    _valid_input_for_transcendental(q, csc_logic.__name__)
    new_value = 1 / sin(q.value)

    return factory(new_value, q.unit)


def sec_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """
    Defines the logic for performing the secant operation on a Quantity
    """
    _valid_input_for_transcendental(q, sec_logic.__name__)
    new_value = 1 / cos(q.value)

    return factory(new_value, q.unit)


def cot_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """
    Defines the logic for performing the cotangent operation on a Quantity
    """
    _valid_input_for_transcendental(q, cot_logic.__name__)
    new_value = 1 / tan(q.value)

    return factory(new_value, q.unit)


""" INVERSE TRIGONOMETRIC FUNCTIONS """


def asin_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """
    Defines the logic for performing the arc sine operation on a Quantity
    """
    _valid_input_for_transcendental(q, asin_logic.__name__)
    _valid_input_for_inverse(q, asin_logic.__name__)
    new_value = asin(q.value)

    return factory(new_value, q.unit)


def acos_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """
    Defines the logic for performing the arc cosine operation on a Quantity
    """
    _valid_input_for_transcendental(q, acos_logic.__name__)
    _valid_input_for_inverse(q, acos_logic.__name__)
    new_value = acos(q.value)

    return factory(new_value, q.unit)


def atan_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """
    Defines the logic for performing the arc tan operation on a Quantity
    """
    _valid_input_for_transcendental(q, atan_logic.__name__)
    new_value = atan(q.value)

    return factory(new_value, q.unit)


def atan2_logic(
    q_y: VPacket, q_x: VPacket, factory: ImplementedQ
) -> VPacket:
    """
    Defines the logic for performing the arc tan 2 operation on a Quantity
    """
    # Ensures both q_y and q_x have the same unit
    q_y.unit_check(q_x)

    # Calculates the new value, unit is always dimensionless
    new_value = atan2(q_y.value, q_x.value)

    return factory(new_value, DIMENSIONLESS)


def acsc_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """
    Defines the logic for performing the arc cosecant operation on a Quantity
    """
    _valid_input_for_transcendental(q, acsc_logic.__name__)
    _valid_input_for_inverse_reciprocal(q, acsc_logic.__name__)

    new_value = asin(1 / q.value)
    return factory(new_value, q.unit)


def asec_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """
    Defines the logic for performing the arc secant operation on a Quantity
    """
    _valid_input_for_transcendental(q, asec_logic.__name__)
    _valid_input_for_inverse_reciprocal(q, asec_logic.__name__)

    new_value = acos(1 / q.value)
    return factory(new_value, q.unit)


def acot_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """
    Defines the logic for performing the arc cotangent operation on a Quantity
    """
    _valid_input_for_transcendental(q, acot_logic.__name__)

    """
    Specific function check: If value == 0, raises a ZeroDivisionError
    """
    if q.value == 0:
        mag = q.value   # Inline length too
        msg = f"Method '{acot_logic.__name__}' requires q != 0, got {mag}"
        raise ZeroDivisionError(msg)

    new_value = atan(1 / q.value)

    return factory(new_value, q.unit)


""" HYPERBOLIC FUNCTIONS """


def sinh_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """ Defines the logic for performing the hyperbolic sine operation """
    _valid_input_for_transcendental(q, sinh_logic.__name__)
    new_value = sinh(q.value)

    return factory(new_value, q.unit)


def cosh_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """ Defines the logic for performing the hyperbolic cosine operation """
    _valid_input_for_transcendental(q, cosh_logic.__name__)
    new_value = cosh(q.value)

    return factory(new_value, q.unit)


def tanh_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """ Defines the logic for performing the hyperbolic tangent operation """
    _valid_input_for_transcendental(q, tanh_logic.__name__)
    new_value = tanh(q.value)

    return factory(new_value, q.unit)


def csch_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """ Defines the logic for performing the hyperbolic cosecant operation """
    _valid_input_for_transcendental(q, csch_logic.__name__)
    new_value = 1 / sinh(q.value)

    return factory(new_value, q.unit)


def sech_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """ Defines the logic for performing the hyperbolic secant operation """
    _valid_input_for_transcendental(q, sech_logic.__name__)
    new_value = 1 / cosh(q.value)

    return factory(new_value, q.unit)


def coth_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """ Defines the logic for performing the hyperbolic cotangent operation """
    _valid_input_for_transcendental(q, coth_logic.__name__)
    new_value = 1 / tanh(q.value)

    return factory(new_value, q.unit)


""" INVERSE HYPERBOLIC FUNCTIONS """


def asinh_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """
    Defines the logic for performing the inverse hyperbolic sine operation
    """
    _valid_input_for_transcendental(q, asinh_logic.__name__)
    new_value = asinh(q.value)

    return factory(new_value, q.unit)


def acosh_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """
    Defines the logic for performing the inverse hyperbolic cosine operation
    """
    _valid_input_for_transcendental(q, acosh_logic.__name__)

    """
    Specific function check: If value < 1, raises a value error
    """
    if q.value < 1:
        mag = q.value
        msg = f"Method '{acosh_logic.__name__} requires q >= 1, got {mag}"
        raise ValueError(msg)

    new_value = acosh(q.value)

    return factory(new_value, q.unit)


def atanh_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """
    Defines the logic for performing the inverse hyperbolic tangent operation
    """
    _valid_input_for_transcendental(q, atanh_logic.__name__)

    """
    Specific function check: If -1 >= value or value >= 1,
    raises a value error
    """
    if -1 >= q.value or q.value >= 1:
        mag = q.value
        msg = f"Method '{atanh_logic.__name__}' requires -1 < q < 1, got {mag}"
        raise ValueError(msg)

    new_value = atanh(q.value)

    return factory(new_value, q.unit)


def acsch_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """
    Defines the logic for performing the inverse hyperbolic cosecant operation
    """
    _valid_input_for_transcendental(q, acsch_logic.__name__)

    """
    Specific function check: If value equals 0, raises a value error
    """
    if q.value == 0:
        mag = q.value   # Inline length too long
        msg = f"Method '{acsch_logic.__name__}' requires q != 0, got {mag}"
        raise ValueError(msg)

    new_value = asinh(1 / q.value)
    return factory(new_value, q.unit)


def asech_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """
    Defines the logic for performing the inverse hyperbolic secant operation
    """
    _valid_input_for_transcendental(q, asech_logic.__name__)

    """
    Specific function check: If value < 0 or value > 1,
    raise a value error
    """
    if q.value > 1 or q.value <= 0:
        mag = q.value   # Inline length too long
        msg = (
            f"Method '{asech_logic.__name__}' requires 0 < q <= 1, got {mag}"
        )
        raise ValueError(msg)

    new_value = acosh(1 / q.value)
    return factory(new_value, q.unit)


def acoth_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """
    Defines the logic for performing the inverse hyperbolic cotangent operation
    """
    _valid_input_for_transcendental(q, acoth_logic.__name__)

    """ Specific function check: If |value| <= 1, raise value error """
    if abs(q.value) <= 1:
        mag = q.value   # Inline length too long
        msg = f"Method '{acoth_logic.__name__}' requires |q| > 1, got {mag}"
        raise ValueError(msg)

    new_value = atanh(1 / q.value)
    return factory(new_value, q.unit)


""" EXPONENTIAL AND LOGARITHMIC FUNCTIONS """


def exp_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """ Defines the logic for performing the exponential operation """
    _valid_input_for_transcendental(q, exp_logic.__name__)
    new_value = exp(q.value)

    return factory(new_value, q.unit)


def log_logic(
    q: VPacket, n: float | int, factory: ImplementedQ
) -> VPacket:
    """ Defines the logic for performing the variable log """
    _valid_input_for_transcendental(q, log_logic.__name__)
    _valid_input_for_logarithms(q, n, log_logic.__name__)

    new_value = log(q.value, n)
    return factory(new_value, q.unit)


def log2_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """ Defines the logic for performing the log 2 """
    _valid_input_for_transcendental(q, log2_logic.__name__)
    _valid_input_for_logarithms(q, 2, log2_logic.__name__)

    new_value = log2(q.value)
    return factory(new_value, q.unit)


def log10_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """ Defines the logic for performing the log 10 """
    _valid_input_for_transcendental(q, log10_logic.__name__)
    _valid_input_for_logarithms(q, 10, log10_logic.__name__)

    new_value = log10(q.value)
    return factory(new_value, q.unit)


def nlog_logic(q: VPacket, factory: ImplementedQ) -> VPacket:
    """" Defines the logic for performing the natural logarithm """
    _valid_input_for_transcendental(q, nlog_logic.__name__)
    _valid_input_for_logarithms(q, e, nlog_logic.__name__)

    new_value = log(q.value)
    return factory(new_value, q.unit)
