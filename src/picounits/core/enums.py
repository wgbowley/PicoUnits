"""
Filename: enums.py
Author: William Bowley
Version: 0.3*

Description:
    This file defines the 'Unit' subclasses
    'FBase' and 'Dimension'. And also the 
    independent class 'PrefixScale'
"""

from __future__ import annotations

from enum import Enum, auto
from dataclasses import dataclass

class PrefixScale(Enum):
    """ Scaling prefixes as powers of 10 for 'Qualities' """
    TERA = 12
    GIGA = 9
    MEGA = 6
    KILO = 3
    HECTO = 2
    DEKA = 1
    BASE = 0
    DECI = -1
    CENTI = -2
    MILLI = -3
    MICRO = -6
    NANO = -9
    PICO = -12

    @property
    def symbol(self) -> str:
        """ Returns the prefix symbol. """
        return _SCALE_SYMBOLS[self]

    def __str__(self) -> str:
        """ Returns name for __str__ dunder method """
        return self.name

    def __repr__(self) -> str:
        """ Displays the scale name and its numerical value """
        return f"<PrefixScale.{self}: 10^{self.value}>"

    @classmethod
    def from_value(cls, power: int) -> tuple[int, PrefixScale]:
        """ Return the PrefixScale for a given power of ten """
        closest_member = min(cls, key=lambda m: abs(m.value - power))
        return (closest_member.value, closest_member)

# Fast mapping for enums and ensure O(1) lookup
_SCALE_SYMBOLS = {
    PrefixScale.TERA: "T",
    PrefixScale.GIGA: "G",
    PrefixScale.MEGA: "M",
    PrefixScale.KILO: "k",
    PrefixScale.HECTO: "h",
    PrefixScale.DEKA: "da",
    PrefixScale.BASE: "",
    PrefixScale.DECI: "d",
    PrefixScale.CENTI: "c",
    PrefixScale.MILLI: "m",
    PrefixScale.MICRO: "μ",
    PrefixScale.NANO: "n",
    PrefixScale.PICO: "p",
}


class FBase(Enum):
    """ Fundamental units """
    TIME = auto()
    LENGTH = auto()
    MASS = auto()
    CURRENT = auto()
    THERMAL = auto()
    AMOUNT = auto()
    LUMINOSITY = auto()
    DIMENSIONLESS = auto()

    @property
    def symbol(self) -> str:
        """ Returns the base unit symbol. """

        # Add code for preferred symbol system (UBASE, SIBase, etc)
        # At the .picounits level after picounits init for example

        return _UBASE_SYMBOLS[self]

    @property
    def order(self) -> int:
        """ Returns the base units under consistent order for notation """
        return _ORDER[self]

    def __str__(self) -> str:
        """ Returns name for __str__ dunder method """
        return self.name

    def __repr__(self) -> str:
        """ Displays the fundamental base """
        return f"<SIBase.{self}>"

# Fast mapping for enums and ensure O(1) lookup
_UBASE_SYMBOLS = {
    FBase.TIME: "t",
    FBase.LENGTH: "l",
    FBase.MASS: "m",
    FBase.CURRENT: "i",
    FBase.THERMAL: "th",
    FBase.AMOUNT: "a",
    FBase.LUMINOSITY: "lu",
    FBase.DIMENSIONLESS: "∅",
}

_SIBASE_SYMBOLS = {
    FBase.TIME: "s",
    FBase.LENGTH: "m",
    FBase.MASS: "kg",
    FBase.CURRENT: "A",
    FBase.THERMAL: "k",
    FBase.AMOUNT: "mol",
    FBase.LUMINOSITY: "cd",
    FBase.DIMENSIONLESS: "∅",
}

_ORDER = {
    FBase.TIME: 2,
    FBase.LENGTH: 1,
    FBase.MASS: 0,
    FBase.CURRENT: 3,
    FBase.THERMAL: 4,
    FBase.AMOUNT: 5,
    FBase.LUMINOSITY: 6,
    FBase.DIMENSIONLESS: 7,
}

@dataclass(slots=True)
class Dimension:
    """ Defines a dimension through 'FBase', 'PrefixScale and 'exponent' """
    base: FBase = FBase.DIMENSIONLESS
    exponent: int = 1

    def __post_init__(self) -> None:
        """ Validates base, exponent and may mutate values. """
        if not isinstance(self.base, FBase):
            msg = f"Dimension base must be FBase, not {type(self.base)}"
            raise TypeError(msg)

        if not isinstance(self.exponent, int):
            msg = f"Dimension exponent must be int, not {type(self.exponent)}"
            raise TypeError(msg)

        # Handle zero exponent: x^0 = 1 (dimensionless)
        if self.exponent == 0:
            self.base = FBase.DIMENSIONLESS
            self.exponent = 1

    @property
    def superscript(self) -> str:
        """ Returns the unicode superscript """
        return str(self.exponent).translate(SUPERSCRIPT_MAP)

    @property
    def name(self) -> str:
        """ Constructs the dimension's name using symbols. """
        if self.exponent == 1:
            return self.base.symbol

        return self.base.symbol + self.superscript

    def __str__(self) -> str:
        """ Returns name for __str__ dunder method """
        return self.name

    def __repr__(self) -> str:
        """ Displays the defined dimension through its components """
        return f"<Dimension name='{self.name}'>"


# Mapping int to unicode for __repr__ & name within Dimension
SUPERSCRIPT_MAP = str.maketrans(
    "0123456789+-",
    "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻"
)
