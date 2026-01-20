"""
Filename: scales.py
Author: William Bowley
Version: 0.6
Clear: Y

Description
    The prefix scale 'PrefixScale' is encoded as a enum
    to enable human readable scales for when displaying
    Quantities to the user interface.
"""

from __future__ import annotations
from typing import Any
from enum import Enum

from picounits.lazy_imports import import_factory, lazy_import

class PrefixScale(Enum):
    """
    Prefix Scale for Quantities:

    Represent the possible prefix scales for quantities.
    Supports normalization of values and scaling
    """
    YOTTA   = 24
    ZETTA   = 21
    EXA     = 18
    PETA    = 15
    TERA    = 12
    GIGA    = 9
    MEGA    = 6
    KILO    = 3
    BASE    = 0
    CENTI   = -2
    MILLI   = -3
    MICRO   = -6
    NANO    = -9
    PICO    = -12
    FEMTO   = -15
    ATTO    = -18
    ZEPTO   = -21
    YOCTO   = -24

    @classmethod
    def from_value(cls, power: int) -> PrefixScale:
        """ Return closest PrefixScale; on ties, prefer smaller scale """
        if not isinstance(power, int):
            msg = f"Power must be an int, not {type(power)}"
            raise TypeError(msg)

        min_distance, closest_member = float('inf'), None

        # O(n) iteration
        for member in cls:
            distance = abs(member.value - power)

            # Update if closer, or tie with smaller scale
            if distance < min_distance or (
                distance == min_distance
                and closest_member is not None
                and member.value < closest_member.value
            ):
                min_distance, closest_member = distance, member

            # Early exit on exact match
            if distance == 0:
                break

        # Fail safe (unlikely): If fails to assign a member, raise error
        if closest_member is None:
            msg = f"No suitable PrefixScale found for power: {power}"
            raise ValueError(msg)

        return closest_member

    @classmethod
    def from_symbol(cls, reference: str) -> PrefixScale | None:
        """
        Compares reference symbol with symbol lookup, if not found returns none
        """
        if not isinstance(reference, str):
            return None

        return _SYMBOLS_TO_SCALE.get(reference)

    @classmethod
    def all_symbols(cls) -> list[str]:
        """ Returns a list of all symbols """
        return list(_SYMBOLS_TO_SCALE.items())

    @property
    def symbol(self) -> str:
        """ Returns the prefix symbol. """
        return _SCALE_SYMBOLS[self]

    def __str__(self) -> str:
        """ Returns name for __str__ dunder method """
        return self.symbol

    def __repr__(self) -> str:
        """ Displays the scale name and its power of 10 """
        return f"<PrefixScale.{self}: 10^{self.value}>"

    def __rmul__(self, other: Any):
        """
        Acts as a syntactic bridge to Quantity to allow for a cleaner API.
        Example: 10 * kilo * LENGTH => Quantity(10, LENGTH, kilo)
        """
        factory = import_factory('PrefixScale.__rmul__')
        unit = lazy_import(
            "picounits.core.unit", "Unit", 'PrefixScale.__rmul__'
        )

        return factory.create(other, unit(), self)


# Fast mapping for enums and ensure o(1) lookup
# Scale symbols dictionary only uses ASCII to ensure easy usage in .uiv files
_SCALE_SYMBOLS = {
    PrefixScale.YOTTA:  "Y",
    PrefixScale.ZETTA:  "Z",
    PrefixScale.EXA:    "E",
    PrefixScale.PETA:   "P",
    PrefixScale.TERA:   "T",
    PrefixScale.GIGA:   "G",
    PrefixScale.MEGA:   "M",
    PrefixScale.KILO:   "k",
    PrefixScale.BASE:   "",
    PrefixScale.CENTI:  "c",
    PrefixScale.MILLI:  "m",
    PrefixScale.MICRO:  "u",
    PrefixScale.NANO:   "n",
    PrefixScale.PICO:   "p",
    PrefixScale.FEMTO:  "f",
    PrefixScale.ATTO:   "a",
    PrefixScale.ZEPTO:  "z",
    PrefixScale.YOCTO:  "y",
}

# Generates a reverse lookup table to ensure o(1) lookup
_SYMBOLS_TO_SCALE = {symbol: scale for scale, symbol in _SCALE_SYMBOLS.items()}
