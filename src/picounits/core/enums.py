"""
Filename: enums.py
Author: William Bowley
Version: 0.1

Description:
    This file defines the 'Unit' subclasses
    'PreFixScale', 'SIBase' and 'Dimension'
"""

from enum import Enum, auto
from dataclasses import dataclass


class PrefixScale(Enum):
    """
    SI metric prefixes as powers of 10. Used to build 'Dimension'
    """
    TERA = 12   # 10¹²
    GIGA = 9    # 10⁹
    MEGA = 6    # 10⁶
    KILO = 3    # 10³
    HECTO = 2   # 10²
    DEKA = 1    # 10¹
    BASE = 0    # 10⁰
    DECI = -1   # 10⁻¹
    CENTI = -2  # 10⁻²
    MILLI = -3  # 10⁻³
    MICRO = -6  # 10⁻⁶
    NANO = -9   # 10⁻⁹
    PICO = -12  # 10⁻¹²

    @property
    def symbol(self) -> str:
        """Returns the SI prefix symbol."""
        return {
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
        }[self]

    def __repr__(self) -> str:
        """ Displays the scale name and its numerical value """
        return f"<Prefix.{self.name}: 10^{self.value}>"


class SIBase(Enum):
    """ SI metric fundamental units expect mass is defined as a gram """
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
        """Returns the SI base unit symbol."""
        return {
            SIBase.SECOND: "s",
            SIBase.METER: "m",
            SIBase.GRAM: "g",
            SIBase.AMPERE: "A",
            SIBase.KELVIN: "K",
            SIBase.MOLE: "mol",
            SIBase.CANDELA: "cd",
            SIBase.DIMENSIONLESS: "∅",
        }[self]

    @property
    def order(self) -> int:
        """ Returns the SI base unit order of important. (0 = Highest)"""
        return {
            SIBase.SECOND: 2,
            SIBase.METER: 1,
            SIBase.GRAM: 0,
            SIBase.AMPERE: 3,
            SIBase.KELVIN: 4,
            SIBase.MOLE: 5,
            SIBase.CANDELA: 6,
            SIBase.DIMENSIONLESS: 7,
        }[self]

    def __repr__(self) -> str:
        """ Displays the fundamental SI metric base """
        return f"<SIBase.{self.name}>"


@dataclass(slots=True)
class Dimension:
    """
    Defines a SI metric dimension through 'SIBase', 'PrefixScale and 'exponent'
    """
    prefix: PrefixScale = PrefixScale.BASE
    base: SIBase = SIBase.DIMENSIONLESS
    exponent: int = 1

    def __post_init__(self):
        """ Checks to ensure prefix, base and exponent are the correct type """
        if not isinstance(self.prefix, PrefixScale):
            msg = (
                f"Dimension prefix cannot be defined with {type(self.prefix)} "
                f"has to be {PrefixScale}"
            )
            raise TypeError(msg)

        if not isinstance(self.base, SIBase):
            msg = (
                f"Dimension base cannot be defined with {type(self.base)} "
                f"has to be {SIBase}"
            )
            raise TypeError(msg)

        if not isinstance(self.exponent, int):
            msg = (
                "Dimension exponent cannot be defined with "
                f"{type(self.exponent)} has to be an {type(int)}"
            )
            raise TypeError(msg)

        # Edge Case: Ensures that bases to the power of zero cancel
        if self.exponent == 0:
            self.base = SIBase.DIMENSIONLESS
            self.exponent = 1

    @property
    def name(self) -> str:
        """Constructs the dimension's SI-style name using symbols."""
        scale = self.prefix.symbol
        base = self.base.symbol

        if self.exponent == 1:
            return f"{scale}{base}"
        return f"{scale}{base}^{self.exponent}"

    def __repr__(self) -> str:
        """ Displays the defined dimension through its components """
        return f"<Dimension name='{self.name}'>"
