"""
Filename: real.py
Author: William Bowley
Version: 0.9
Clear: X

Description:
    Defines the Real Packet Class which is
    comprised of a Value, Unit and prefixScale.
"""

from math import log10, ceil
from typing import Any
from dataclasses import dataclass

from picounits.core.unit import Unit
from picounits.core.scales import PrefixScale

from picounits.core.quantities.packet import Packet
from picounits.core.quantities.scalars.scalar import ScalarPacket


@dataclass(slots=True)
class RealPacket(ScalarPacket):
    """
    A Real Packet: A prefix, value (integer or float) and Unit

    NOTE: Prefix is init-only, value is held in absolute form
    """
    def __post_init__(self, prefix: PrefixScale) -> None:
        """ Validates value and unit, then mutates value to BASE """
        if not isinstance(self.value, (int, float)):
            try:
                # Provides a custom error message for the import injection
                from picounits.core.quantities.factory import Factory
            except ImportError as error:
                msg = (
                    "Could not import 'Factory' for RealPacket.__post_init__"
                    "This usually means picounits was not installed correctly "
                )
                raise ImportError(msg) from error

            # Attempts to pass the value to the correct type
            return Factory.create(self.value, self.unit, prefix)

        if not isinstance(self.unit, Unit):
            msg = f"Unit must be of type 'Unit', not {type(self.unit)}"
            raise TypeError(msg)

        if not isinstance(prefix, PrefixScale):
            msg = f"Prefix must be of type PrefixScale, not {type(prefix)}"
            raise TypeError(msg)

        # Mutates prefix to PrefixScale.BASE and scales value
        if prefix == PrefixScale.BASE:
            return

        # Ex.  Kilo (3) - BASE (0) = 3 Hence scaling of 10^3
        prefix_difference = prefix.value - PrefixScale.BASE.value
        factor = 10 ** prefix_difference
        self.value *= factor

    @property
    def name(self) -> str:
        """ Returns the packet name as value + prefix(unit) """
        value, prefix = self._normalize()
        return f"{value} {prefix}({self.unit.name})"

    @property
    def magnitude(self) -> int | float:
        """ Returns the mathematical absolute value """
        return abs(self.value)

    def _normalize(self) -> tuple[float | int, PrefixScale]:
        """ Normalizes the value for packet name representation """
        value = self.value
        if value == 0:
            # Handles division by zero edge case
            return 0, PrefixScale.BASE

        # Uses log10 to approximate power
        magnitude = abs(value)
        prefix_power = int(log10(magnitude))
        test_value = magnitude / (10 ** prefix_power)

        if test_value <= 1.0:
            prefix_power -= 1

        # O(n) prefix lookup & calculation of new value
        closest = PrefixScale.from_value(prefix_power)
        value /= 10 ** closest.value

        return value, closest

    def __format__(self, format_spec: str) -> str:
        """ Formats the string based on user input through 'format_spec'"""
        value, prefix = self._normalize()
        formatted_value = format(value, format_spec)

        return f"{formatted_value} {prefix}({self.unit.name})"

    def __ceil__(self) -> Packet:
        """ Defines the behavior for ceiling method """
        try:
            # Provides a custom error message for the import injection
            from picounits.core.quantities.factory import Factory
        except ImportError as error:
            msg = (
                "Could not import 'Factory' for RealPacket.__ceil__"
                "This usually means picounits was not installed correctly "
            )
            raise ImportError(msg) from error

        return Factory.create(ceil(self.value), self.unit)

    def __eq__(self, other: Any) -> bool:
        """ Defines the behavior for equality comparison """
        q2 = self._get_other_packet(other)
        if self.unit != q2.unit:
            # Unit equality matters
            return False

        return self.value == q2.value

    @staticmethod
    def _valid_comparison(q1: Packet, q2: Packet) -> None:
        """
        Raises a ValueError if q1.unit != q2.unit, if not returns none
        """
        if q1.unit == q2.unit:
            return

        msg = f"Cannot compare different units, {q1.unit} != {q2.unit}"
        raise ValueError(msg)

    def __lt__(self, other: Any) -> bool:
        """ Defines the behavior for less than comparison """
        q2 = self._get_other_packet(other)
        self._valid_comparison(self, q2)

        return self.value < q2.value

    def __le__(self, other: Any) -> bool:
        """ Defines the behavior for less than or equal to comparison """
        q2 = self._get_other_packet(other)
        self._valid_comparison(self, q2)

        return self.value <= q2.value

    def __gt__(self, other: Any) -> bool:
        """ Defines the behavior for greater than comparison """
        q2 = self._get_other_packet(other)
        self._valid_comparison(self, q2)

        return self.value > q2.value

    def __ge__(self, other: Any) -> bool:
        """ Defines the behavior for greater than or equal to comparison """
        q2 = self._get_other_packet(other)
        self._valid_comparison(self, q2)

        return self.value >= q2.value
