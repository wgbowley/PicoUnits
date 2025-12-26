"""
Filename: enums.py
Author: William Bowley
Version: 0.4
Clear: Y

Description:
    Defines the Dimension dataclass,
    which is comprised of a fundamental unit
    and exponent.

    The fundamental unit 'FBASE' is
    encoded as a enum to enable dimensional
    analysis, custom ordering and symbols
"""

from __future__ import annotations

from enum import Enum, auto
from functools import lru_cache
from dataclasses import dataclass, field

from picounits.configuration.picounits import MAX_EXPONENT

try:
    # Ensures picounits works even with preferences issues
    from picounits.configuration.config import get_base_symbols, get_base_order
except ImportError:
    def get_base_symbols() -> dict[str, str]:
        """ placeholder """
        return {}

    def get_base_order() -> dict[str, int]:
        """ placeholder """
        return {}


@lru_cache(maxsize=1)
def _symbols() -> dict[str, str]:
    """ Caches the symbols for FBase """
    return get_base_symbols()


@lru_cache(maxsize=1)
def _order() -> dict[str, int]:
    """ Caches the order for FBase """
    return get_base_order()


class FBase(Enum):
    """
    Fundamental SI base dimensions:

    Represents the seven SI base units plus dimensionless quantities.
    Supports custom symbols and ordering via configurations
    """
    TIME    = auto()
    LENGTH  = auto()
    MASS    = auto()
    CURRENT = auto()
    THERMAL = auto()
    AMOUNT  = auto()
    LUMINOSITY  = auto()
    DIMENSIONLESS = auto()

    @property
    def symbol(self) -> str:
        """ Returns the base unit symbol. """
        return _symbols().get(self.name, _SIBASE_SYMBOLS[self])

    @property
    def order(self) -> int:
        """ Returns the base units under consistent order for notation """
        return _order().get(self.name, _ORDER[self])

    @classmethod
    def from_symbol(cls, reference: str) -> FBase | None:
        """
        Compares reference symbol with symbol lookup, if not found returns none
        """
        if not isinstance(reference, str):
            return None

        # Primary: Tries preferred symbols
        for member in cls:
            preferred = _symbols().get(member.name)
            if preferred and preferred == reference:
                return member

        # Fallback: check standard symbols
        for enum_member, symbol in _SIBASE_SYMBOLS.items():
            if symbol == reference:
                return enum_member

        return None

    def __str__(self) -> str:
        """ Returns name for __str__ dunder method. """
        return self.name

    def __repr__(self) -> str:
        """ Displays the fundamental base. """
        return f"<FBase.{self.name}>"


@dataclass(frozen=True, slots=True)
class Dimension:
    """
    A Physical dimension: Base unit raised to an signed integer power.

    Args:
        base: The fundamental unit type (FBase Enum)
        exponent: Integer power, limited to +/- 10
    """
    base: FBase = FBase.DIMENSIONLESS
    exponent: int = 1
    # Note _name_cache is an implementation detail, zero impact on correctness
    _name_cache: str = field(init=False, repr=False, default="")

    def __post_init__(self) -> None:
        """ Validates base, exponent and may mutate values. """
        if not isinstance(self.base, FBase):
            msg = f"Dimension base must be FBase, not {type(self.base)}"
            raise TypeError(msg)

        if not isinstance(self.exponent, int):
            msg = f"Dimension exponent must be int, not {type(self.exponent)}"
            raise TypeError(msg)

        # Handle exponent limit
        if abs(self.exponent) > MAX_EXPONENT:
            msg = f"Exponent {self.exponent}>{MAX_EXPONENT}, exceeded limit"
            raise ValueError(msg)

        # Handle zero exponent: x^0 = 1 (dimensionless)
        if self.exponent == 0:
            # NOTE: Mutates only during init to ensure correctness
            object.__setattr__(self, "base", FBase.DIMENSIONLESS)
            object.__setattr__(self, "exponent", 1)

        # Dimensionless quantities have no meaningful exponent
        if self.base == FBase.DIMENSIONLESS:
            # NOTE: Mutates only during init to ensures correctness
            object.__setattr__(self, "exponent", 1)

        name = (
            self.base.symbol if self.exponent == 1
            else self.base.symbol + self.superscript
        )

        # NOTE: Caches name to improve performance uses mutation
        object.__setattr__(self, "_name_cache", name)

    @property
    def superscript(self) -> str:
        """ Returns the unicode superscript. """
        return str(self.exponent).translate(SUPERSCRIPT_MAP)

    @property
    def name(self) -> str:
        """ Constructs the dimension's name using symbols. """
        return self._name_cache

    @classmethod
    def dimensionless(cls) -> Dimension:
        """Factory method for dimensionless. """
        return cls(FBase.DIMENSIONLESS, 1)

    def __str__(self) -> str:
        """ Returns name for __str__ dunder method. """
        return self.name

    def __repr__(self) -> str:
        """ Displays the defined dimension through its components. """
        return f"<Dimension name='{self.name}'>"


# Mapping int to unicode for __repr__ & name within Dimension
SUPERSCRIPT_MAP = str.maketrans("0123456789+-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻")

# Standard SI Secondary fallbacks (used when not overridden in preferences)
_SIBASE_SYMBOLS = {
    FBase.TIME: "s",
    FBase.LENGTH: "m",
    FBase.MASS: "kg",
    FBase.CURRENT: "A",
    FBase.THERMAL: "K",
    FBase.AMOUNT: "mol",
    FBase.LUMINOSITY: "cd",
    FBase.DIMENSIONLESS: "∅",
}

# Preferred order for consistent dimensional notation (e.g., kg·m²/s²)
# Mass first (0), then length (1), time (2), etc.
_ORDER = {
    FBase.MASS: 0,
    FBase.LENGTH: 1,
    FBase.TIME: 2,
    FBase.CURRENT: 3,
    FBase.THERMAL: 4,
    FBase.AMOUNT: 5,
    FBase.LUMINOSITY: 6,
    FBase.DIMENSIONLESS: 7,
}
