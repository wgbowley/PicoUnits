"""
Filename: conversion.py
Author: William Bowley
Version: 0.1

Description:
    This file contains the helper
    functions for quality when doing
    unit conversions.
"""

from picounits.core.unit import Unit


def _valid_conversion(old: Unit, new: Unit) -> None:
    """ Validates that the two units are compatible for conversion """

    # Checks for same length between units
    if old.length != new.length:
        msg = (
            "Conversion check failed: Units must have the same length "
            f"({old.length} != {new.length})"
        )
        raise ValueError(msg)

    # Checks correctness between units
    old_lookup = {(dim.base, dim.exponent): dim for dim in old.dimensions}
    new_lookup = {(dim.base, dim.exponent): dim for dim in new.dimensions}

    if old_lookup.keys() != new_lookup.keys():
        msg = (
            "Conversion check failed: Base Units and Exponents do not match "
            f"({old_lookup.keys()} != {new_lookup.keys()})"
        )
        raise ValueError(msg)


def _computes_scale(old: Unit, new: Unit) -> float:
    """ Computes the conversion factor between 'old' to 'new' unit """
    lookup = {(dim.base, dim.exponent): dim for dim in new.dimensions}
    factor = 1.0

    for old_dim in old.dimensions:
        key = (old_dim.base, old_dim.exponent)
        new_dim = lookup[key]

        # Calculates the prefix difference
        # Ex. Base (0) - Kilo (3) = -3 Hence base exponent of -3
        prefix_diff = old_dim.prefix.value - new_dim.prefix.value

        # Scales the prefix_diff by the base exponent (Power of a power)
        total_exponent = prefix_diff * old_dim.exponent
        factor *= 10 ** total_exponent

    return factor


def conversion(
    magnitude: float | int, old: Unit, new: Unit
) -> tuple[float | int, Unit]:
    """ Converts a numeric value from 'old' to 'new' unit """
    _valid_conversion(old, new)
    factor = _computes_scale(old, new)

    # Ensures integer arithmetic occurs if applicable
    result = magnitude * factor
    result = int(result) if result == int(result) else result
    return result, new
