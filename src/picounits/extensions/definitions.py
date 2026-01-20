"""
Filename: definitions.py
Author: William Bowley
Version: 0.2

Description:
    Defines the mathematical operators for
    usage by the converter when parsing .uiv format.
"""

from __future__ import annotations
from enum import Enum, auto

class ParserError(ValueError):
    """ Exception for parser errors when parsing """
    def __init__(self, caller: str, error: str):
        """ Returns a custom error message """
        msg = f"'{caller}' raised error: {error}. "
        super().__init__(msg)


class Operations(Enum):
    """ Map of Mathematical Operations for Units """
    MULTIPLICATION = auto()
    POWER = auto()
    DIVIDED = auto()

    @property
    def symbol(self) -> str:
        """ Returns the operation symbol via direct lookup """
        return _LOOKUP_OPERATORS.get(self)[0]

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
            msg = f"'{char}' is an unknown operator. Supported operators are {ops}"
            raise ParserError(cls.__name__, msg)

        return operator

    @classmethod
    def check_unicode_power(cls, power: str) -> int | None:
        """ Returns converted unicode power """
        return SUPERSCRIPT_MAP[power]

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
SUPERSCRIPT_MAP = {
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
_LOOKUP_OPERATORS = {}
for symbol, op in _LOOKUP_STRINGS.items():
    _LOOKUP_OPERATORS.setdefault(op, []).append(symbol)
