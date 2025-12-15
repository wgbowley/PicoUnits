"""
Filename: units.py
Author: William Bowley
Version: 0.3

Description:
    This file defines the 'Unit' dataclass
    and defines it subclasses 'PreFixScale',
    'SIBase' and 'Dimension'
"""

from __future__ import annotations

from typing import Any
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
        """ Returns the SI base unit order of important. """
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


class Unit:
    """
    Defines a SI metric unit composed of a singular or multiple 'Dimension'.
    """
    def __init__(self, *dimensions: Dimension) -> None:
        if not dimensions:
            msg = "A unit cannot be defined without any dimensions"
            raise RuntimeError(msg)

        for dim in dimensions:
            if not isinstance(dim, Dimension):
                msg = (
                    f"A unit cannot be defined with {type(dim)} "
                    f"has to be {Dimension}"
                )
                raise ValueError(msg)

        self.dimensions: list[Dimension] = list(dimensions)

        # Removes DIMENSIONLESS if there are other dimensions
        if self.length > 1:
            self.dimensions = [
                dim for dim in self.dimensions
                if dim.base != SIBase.DIMENSIONLESS
            ]

        # Raises error if SIbase is duplicated in the unit definition
        _duplicated_bases = set()
        for dim in self.dimensions:
            if dim.base in _duplicated_bases:
                msg = f"Cannot define a unit with duplicated bases: {dim.base}"
                raise RuntimeError(msg)
            _duplicated_bases.add(dim.base)

    @property
    def length(self) -> int:
        """ Returns the number of dimensions within the unit """
        return len(self.dimensions)

    @property
    def name(self) -> str:
        """ Returns the units name based on its dimensions """
        self.dimensions = sorted(
            self.dimensions,
            key=lambda item: item.base.order
        )

        return " ".join([str(dim.name) for dim in self.dimensions])

    """ Dunder methods for forward/reverse arithmetic and others """

    def __mul__(self, other: Unit) -> Unit:
        """ Defines behavior for the forward multiplication operator """
        return None

    def __rmul__(self, other: Any) -> None:
        """ Defines behavior for the right-hand multiplication """
        msg = f"Cannot multiply a {type(other)} by {type(self).__name__}"
        raise TypeError(msg)

    def __rtruediv__(self, other: Any) -> None:
        """ Defines behavior for the right-hand true division """
        msg = f"Cannot true divide a {type(other)} by {type(self).__name__}"
        raise TypeError(msg)

    def __rpow__(self, other: Any) -> None:
        """ Defines behavior for the right-hand power """
        msg = f"Cannot raise a {type(other)} by {type(self).__name__}"
        raise TypeError(msg)

    def __eq__(self, other) -> bool:
        """ Checks equality between units """
        if not isinstance(other, Unit):
            return False
        if self.length != other.length:
            return False

        self_set = {(d.base, d.prefix, d.exponent) for d in self.dimensions}
        other_set = {(d.base, d.prefix, d.exponent) for d in other.dimensions}
        return self_set == other_set

    def __hash__(self) -> int:
        """
        Calculates a hash based on the dimensions independent of internal order
        """
        dim_tuples = {(d.base, d.prefix, d.exponent) for d in self.dimensions}
        return hash(frozenset(dim_tuples))

    def __repr__(self) -> str:
        """ Displays the formatted unit representation """
        return self.name


""" Helper functions for unit scaling and conversion """


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