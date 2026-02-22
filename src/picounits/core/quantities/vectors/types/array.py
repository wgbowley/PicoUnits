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
    array, ndarray, floating, integer, ceil, linalg, floor,
    log10, isfinite, abs as np_abs, max as np_max, append as np_append
)

from picounits.core.unit import Unit
from picounits.core.scales import PrefixScale

from picounits.core.quantities.packet import Packet
from picounits.core.quantities.vectors.vector import VectorPacket

from picounits.lazy_imports import import_factory


@dataclass(slots=True, repr=False, unsafe_hash=True)
class ArrayPacket(VectorPacket):
    """
    A Array Packet: A prefix, array and a unit

    NOTE: Prefix is init-only, value is held in absolute form
    """
    def __post_init__(self, prefix: PrefixScale) -> None:
        """ Validates value and unit, then mutates values to BASE """
        if not isinstance(self.value, (list, tuple, ndarray)):
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
                if isinstance(item, complex):
                    msg = "Cannot create a vector of complex numbers"
                    raise TypeError(msg)

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
        """ Returns the magnitude of vector with units """
        factory = import_factory("ArrayPacket.magnitude")

        value = float(linalg.norm(self.value))
        return factory.create(value, self.unit)

    def append(self, item: Packet) -> None:
        """ Appends a Packet to the array. """
        if not isinstance(item, Packet):
            raise TypeError(f"append() argument must be a Packet, not {type(item).__name__}")

        if isinstance(item.value, complex):
            raise TypeError(f"Vectors cannot element thats a complex number, got {item}")

        self.unit_check(item)
        self.value = np_append(self.value, item.value)

    def _normalize(self) -> tuple[complex, PrefixScale]:
        """ Normalizes the value for packet name representation """
        if self.value.size == 0 or self.unit == Unit.dimensionless():
            return self.value, PrefixScale.BASE

        # Focus on the 'peak' magnitude to define the scale
        max_mag = np_max(np_abs(self.value))

        if max_mag == 0 or not isfinite(max_mag):
            return self.value, PrefixScale.BASE

        # Get the prefix for the largest element
        peak_power = int(floor(log10(max_mag)))
        closest = PrefixScale.from_value(peak_power)

        return self.value / (10 ** closest.value), closest

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
