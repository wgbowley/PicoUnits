"""
Filename: operations.py

Description:
    Defines the mathematical operators 
    for usage during construction of units
    when parsing .ut & .uiv dsl formats.
"""

from __future__ import annotations
from enum import Enum, auto

from picounits.extensions.utilities.errors import UnknownOperator, AmbiguousPower


class Operations(Enum):
    """ Map of Mathematical Operations for Units """
    MULTIPLICATION = auto()
    POWER = auto()
    DIVIDED = auto()

    @property
    def symbol(self) -> str:
        """ Returns the value operation symbol via direct lookup """
        return _LOOKUP_OPERATORS.get(self)

    @property
    def _repr_name(self) -> str:
        """ Returns the operator object name """
        return f"<Operations type={self.name}, symbol={self.symbol}>"

    @classmethod
    def from_symbol(cls, char: str) -> Operations:
        """ Creation of operator object via symbol direct lookup """
        operator = _LOOKUP_STRINGS.get(char)
        if operator is None:
            ops = list(_LOOKUP_STRINGS.keys())
            raise UnknownOperator(char, ops)

        return operator

    @classmethod
    def validate_unicode_usage(cls, tokens: list[str]) -> None:
        """ Ensures non mixing of `^` with unicode superscripts """
        has_caret = "^" in tokens
        has_unicode = any(t in _SUPERSCRIPT_MAP for t in tokens)

        if has_caret and has_unicode:
            msg = "Mixing `^` and unicode superscripts in unit expression"
            raise AmbiguousPower(msg)

    @classmethod
    def check_unicode_power(cls, power: str) -> int | False:
        """ Returns converted unicode power """
        try:
            return _SUPERSCRIPT_MAP[power]

        except KeyError:
            return False

    @classmethod
    def all_symbols(cls) -> list[str]:
        """ Returns a list of all symbols """
        return list(_LOOKUP_STRINGS.keys())

    def __repr__(self) -> str:
        """ Return string representation for terminal"""
        return self._repr_name

    def __str__(self) -> str:
        """ Return string representation """
        return self._repr_name


# Direct lookup table for string notation
_LOOKUP_STRINGS = {
    "*": Operations.MULTIPLICATION,
    "x": Operations.MULTIPLICATION,
    "·": Operations.MULTIPLICATION,
    "∙": Operations.MULTIPLICATION,
    "/": Operations.DIVIDED,
    "÷": Operations.DIVIDED,
    "^": Operations.POWER,
    "⁰": Operations.POWER,
    "¹": Operations.POWER,
    "²": Operations.POWER,
    "³": Operations.POWER,
    "⁴": Operations.POWER,
    "⁵": Operations.POWER,
    "⁶": Operations.POWER,
    "⁷": Operations.POWER,
    "⁸": Operations.POWER,
    "⁹": Operations.POWER,
}


# Unicode lookup table
_SUPERSCRIPT_MAP = {
    "⁰": 0,
    "¹": 1,
    "²": 2,
    "³": 3,
    "⁴": 4,
    "⁵": 5,
    "⁶": 6,
    "⁷": 7,
    "⁸": 8,
    "⁹": 9,
}


# Direct lookup table for operator enum to string notation
_LOOKUP_OPERATORS: dict[Operations, list[str]] = {}
for symbol, operation in _LOOKUP_STRINGS.items():
    if operation not in _LOOKUP_OPERATORS:
        _LOOKUP_OPERATORS[operation] = []

    _LOOKUP_OPERATORS[operation].append(symbol)
