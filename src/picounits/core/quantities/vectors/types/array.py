"""
Filename: array.py
Author: William Bowley
Version: 0.1
Clear: X

Description:
    Defines the Array Packet Class which is
    comprised of a Value, Unit and prefixScale.
"""


from __future__ import annotations
from dataclasses import dataclass

from numpy import (
    array, floating, integer, ceil, linalg, floor,
    log10, unique, argmax, any as NpAny
)

from picounits.core.unit import Unit
from picounits.core.scales import PrefixScale

from picounits.core.quantities.packet import Packet
from picounits.core.quantities.vectors.vector import VectorPacket

from picounits.lazy_imports import import_factory


@dataclass(slots=True, repr=False)
class ArrayPacket(VectorPacket):
    """
    A Array Packet: A prefix, array and a unit

    NOTE: Prefix is init-only, value is held in absolute form
    """
    def __post_init__(self, prefix: PrefixScale) -> None:
        """ Validates value and unit, then mutates values to BASE """
        if not isinstance(self.value, (list, tuple, array)):
            factory = import_factory("ArrayPacket.__post_init__")

            # Attempts to pass the value to the correct type
            return factory.create(self.value, self.unit, prefix)

        if not isinstance(self.unit, Unit):
            msg = f"Unit must be of type 'Unit', not {type(self.unit)}"
            raise TypeError(msg)

        if not isinstance(prefix, PrefixScale):
            msg = f"Prefix must be of type PrefixScale, not {type(prefix)}"
            raise TypeError(msg)

        # Mutates prefix to PrefixScale.BASE and scales value
        factor = 1
        if prefix != PrefixScale.BASE:
            # Ex.  Kilo (3) - BASE (0) = 3 Hence scaling of 10^3
            prefix_difference = prefix.value - PrefixScale.BASE.value
            factor = 10 ** prefix_difference

        # Converts the input to a non-scaled ndarry
        self._quantity_conversion(factor)

    def _quantity_conversion(self, factor: int) -> None:
        """Strip packet wrappers and ensure we have numeric types."""
        new_value: list = []
        for item in self.value:
            if isinstance(item, Packet):
                self.unit_check(item) # Use Packet's built-in unit checker
                new_value.append(item.value * factor)

            elif isinstance(item, (int, float, integer, floating)):
                new_value.append(item)

            else:
                msg = f"Cannot convert {type(item)} to ArrayPacket value"
                raise TypeError(msg)

        self.value = array(new_value) * factor

    @property
    def name(self) -> str:
        """ Returns the packet name as value + prefix(unit) """
        value, prefix = self._normalize()
        return f"{value} {prefix}({self.unit.name})"

    @property
    def magnitude(self) -> float:
        return float(linalg.norm(self.value))

    def _normalize(self) -> tuple[complex, PrefixScale]:
        """ Normalizes the value for packet name representation """
        if self.value.size == 0:
            # Handles division by zero edge case
            return self.value, PrefixScale.BASE

        if self.unit == Unit.dimensionless():
            # Handles dimensionless values via non-normalization
            return self.value, PrefixScale.BASE

        # Uses log10 to approximate power
        magnitudes = abs(self.value)
        mask = magnitudes > 0

        if not NpAny(mask):
            return self.value, PrefixScale.BASE

        # Uses log10 to approximate power
        powers = floor(log10(magnitudes[mask])).astype(int)

        # Finds the most common power of the set
        vals, counts = unique(powers, return_counts=True)
        most_common_power = vals[argmax(counts)]

        # O(n) prefix lookup & calculation of new value
        closest = PrefixScale.from_value(int(most_common_power))

        # Uses most common power to scale the set
        normalized_values = self.value / (10 ** closest.value)

        return normalized_values, closest

    def __format__(self, format_spec: str) -> str:
        """ Formats the string based on user input through 'format_spec'"""
        value, prefix = self._normalize()
        formatted_value = format(value, format_spec)

        return f"{formatted_value} {prefix}({self.unit.name})"

    def __ceil__(self) -> Packet:
        """ Defines the behavior for ceiling method """
        factory = import_factory("ArrayPacket.__ceil__")
        return factory.create(ceil(self.value), self.unit)

    def __repr__(self) -> str:
        """ Displays the packet name """
        return str(self.name)
