"""
Filename: scales.py
Author: William Bowley
Version: 0.5
Clear: N

Description:
    This file defines the 'PrefixScale' enum
"""

from __future__ import annotations

from enum import Enum


class PrefixScale(Enum):
    """ Scaling prefixes as powers of 10 for 'Qualities' """
    YOTTA   = 24
    ZETTA   = 21
    EXA     = 18
    PETA    = 15
    TERA    = 12
    GIGA    = 9
    MEGA    = 6
    KILO    = 3
    HECTO   = 2
    DEKA    = 1
    BASE    = 0
    DECI    = -1
    CENTI   = -2
    MILLI   = -3
    MICRO   = -6
    NANO    = -9
    PICO    = -12
    FEMTO   = -15
    ATTO    = -18
    ZEPTO   = -21
    YOCTO   = -24

    @property
    def symbol(self) -> str:
        """ Returns the prefix symbol. """
        return _SCALE_SYMBOLS[self]

    @classmethod
    def from_value(cls, power: int) -> tuple[int, PrefixScale]:
        """ Return the PrefixScale for a given power of ten """
        closest_member = min(cls, key=lambda m: abs(m.value - power))
        return (closest_member.value, closest_member)

    @classmethod
    def from_symbol(cls, reference: str) -> PrefixScale | None:
        """ Compares reference symbol with symbol lookup """
        if isinstance(reference, str):
            for enum_member, symbol in _SCALE_SYMBOLS.items():
                if symbol == reference:
                    return enum_member

        return None

    def __str__(self) -> str:
        """ Returns name for __str__ dunder method """
        return self.name

    def __repr__(self) -> str:
        """ Displays the scale name and its numerical value """
        return f"<PrefixScale.{self}: 10^{self.value}>"

    def __rmul__(self, other: float | int):
        """ Defines behavior for the right-hand multiplication """
        from picounits.core.qualities import Quantity

        return Quantity(magnitude=other, prefix=self)


# Fast mapping for enums and ensure lookup
_SCALE_SYMBOLS = {
    PrefixScale.YOTTA:  "Y",
    PrefixScale.ZETTA:  "Z",
    PrefixScale.EXA:    "E",
    PrefixScale.PETA:   "P",
    PrefixScale.TERA:   "T",
    PrefixScale.GIGA:   "G",
    PrefixScale.MEGA:   "M",
    PrefixScale.KILO:   "k",
    PrefixScale.HECTO:  "h",
    PrefixScale.DEKA:   "da",
    PrefixScale.BASE:   "",
    PrefixScale.DECI:   "d",
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
