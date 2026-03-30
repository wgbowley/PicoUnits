"""
Filename: arithmetic.py
Author: William Bowley
Version: 0.2

Description:
    Defines the methods for operation instance methods 
    for vector quantities
"""

from numpy import ndarray, dot as np_dot, cross as np_cross, arccos

from picounits.core.unit import Unit

from picounits.core.quantities.packet import Packet
from picounits.core.quantities.factory import Factory


def _temporary_numpy_requirement(q1: Packet, q2: Packet) -> None:
    """
    NOTE: This method should be replaced with a conversion layer
    that handles multiple vector representations (numpy, symbolic, etc.)
    """
    if not isinstance(q1.value, ndarray) or not isinstance(q2.value, ndarray):
        msg = (
            f"Vector operations currently only support numpy arrays. "
            f"Got {type(q1.value).__name__} and {type(q2.value).__name__}. "
            f"Cannot perform operation between {q1} and {q2}"
        )
        raise NotImplementedError(msg)


def dot(q1: Packet, q2: Packet) -> Packet:
    """ Computes the dot product of two vector packets """
    Factory.category_check(q1, q2)

    # NOTE: This method should be replaced with a conversion layer
    _temporary_numpy_requirement(q1, q2)

    # Computes the dot product of values and multiples units
    result_value = np_dot(q1.value, q2.value)
    result_unit = q1.unit * q2.unit

    return Factory.create(result_value, result_unit)


def cross(q1: Packet, q2: Packet) -> Packet:
    """ Computes the cross product of two vector packets """
    Factory.category_check(q1, q2)

    # NOTE: This method should be replaced with a conversion layer
    _temporary_numpy_requirement(q1, q2)

    if q1.value.size != 3 or q2.value.size != 3:
        msg = "Cross product is only defined for 3D vectors"
        raise ValueError(msg)

    # Compute cross product of values
    result_value = np_cross(q1.value, q2.value)

    # Compute resulting unit (multiplication of units)
    result_unit = q1.unit * q2.unit
    return Factory.create(result_value, result_unit)

def angle_between(q1: Packet, q2: Packet) -> Packet:
    """ Computes the angle between q1 and q2 vectors. Returns radians """
    Factory.category_check(q1, q2)

    # NOTE: This method should be replaced with a conversion layer
    _temporary_numpy_requirement(q1, q2)

    # Check units are compatible
    q1.unit_check(q2)

    # Compute magnitudes
    q1_mag = q1.magnitude
    q2_mag = q2.magnitude

    if q1_mag == 0 or q2_mag == 0:
        msg = "Cannot compute angle with zero-magnitude vector"
        raise ValueError(msg)

    # Compute dot product and normalize by magnitudes
    dot_product = np_dot(q1.value, q2.value)
    cos_angle = dot_product / (q1_mag * q2_mag)

    # Clamp to [-1, 1] to handle floating point errors
    cos_angle = max(-1.0, min(1.0, cos_angle))

    angle_rad = arccos(cos_angle)
    return Factory.create(angle_rad, Unit.dimensionless())


def normalize(q1: Packet) -> Packet:
    """ Returns a unit vector in the same direction as this vector """
    mag = q1.magnitude

    if mag == 0:
        msg = "Cannot normalize a zero-magnitude vector"
        raise ValueError(msg)

    # Divide value by magnitude to get unit vector
    normalized_value = q1.value / mag
    return Factory.create(normalized_value, q1.unit)
