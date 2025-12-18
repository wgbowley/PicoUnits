"""
Filename: enums.py
Author: William Bowley
Version: 0.2

Description:
    This file defines the 'Unit' subclasses
    'FBase' and 'Dimension'. And also the 
    independent class 'PrefixScale'
"""

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
    SECOND = auto()             # Time
    METER = auto()              # Length
    GRAM = auto()               # Mass
    AMPERE = auto()             # Electric Current
    KELVIN = auto()             # Temperature
    MOLE = auto()               # Amount of a substance
    CANDELA = auto()            # Luminous Intensity
    DIMENSIONLESS = auto()      # Non-physical quantity

    @property
    def symbol(self) -> str:
        """ Returns the base unit symbol. """
        return _BASE_SYMBOLS[self]

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
_BASE_SYMBOLS = {
    FBase.SECOND: "s",
    FBase.METER: "m",
    FBase.GRAM: "g",
    FBase.AMPERE: "A",
    FBase.KELVIN: "K",
    FBase.MOLE: "mol",
    FBase.CANDELA: "cd",
    FBase.DIMENSIONLESS: "∅",
}

# Fast mapping for enums and ensure O(1) lookup
_ORDER = {
    FBase.SECOND: 2,
    FBase.METER: 1,
    FBase.GRAM: 0,
    FBase.AMPERE: 3,
    FBase.KELVIN: 4,
    FBase.MOLE: 5,
    FBase.CANDELA: 6,
    FBase.DIMENSIONLESS: 7,
}

@dataclass(slots=True)
class Dimension:
    """ Defines a dimension through 'FBase', 'PrefixScale and 'exponent' """
    base: FBase = FBase.DIMENSIONLESS
    exponent: int = 1

    def __post_init__(self):
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
    def name(self) -> str:
        """ Constructs the dimension's name using symbols. """
        if self.exponent == 1:
            return self.base.symbol

        return f"{self.base.symbol}^{self.exponent}"

    def __str__(self) -> str:
        """ Returns name for __str__ dunder method """
        return self.name

    def __repr__(self) -> str:
        """ Displays the defined dimension through its components """
        return f"<Dimension name='{self.name}'>"
