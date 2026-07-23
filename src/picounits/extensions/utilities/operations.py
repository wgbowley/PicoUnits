"""
Filename: operations.py

Description:
    Defines the mathematical operators 
    for usage during construction of units
    when parsing .ut & .uiv dsl formats.
"""

from __future__ import annotations
from enum import Enum, auto

from picounits.extensions.utilities.errors import UnknownOperator


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
}


# Direct lookup table for operator enum to string notation
_LOOKUP_OPERATORS: dict[Operations, list[str]] = {}
for symbol, operation in _LOOKUP_STRINGS.items():
    if operation not in _LOOKUP_OPERATORS:
        _LOOKUP_OPERATORS[operation] = []

    _LOOKUP_OPERATORS[operation].append(symbol)
