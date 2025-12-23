"""
Filename: parser.py
Author: William Bowley
Version: 0.1

Description:
    Defines the Parser for .uiv (Unit-Informed Values) files
"""

from __future__ import annotations

from typing import Any
from enum import Enum, auto

from picounits.core.unit import Unit
from picounits.constants import DIMENSIONLESS
from picounits.core.qualities import Quantity
from picounits.core.enums import PrefixScale, FBase, Dimension


class Operators(Enum):
    """ Operations for 'Matcher' """
    MULTIPLICATION = auto()
    POWER = auto()
    DIVIDED = auto()

    @property
    def symbol(self) -> str:
        """ Returns the operation symbol """
        return _OPERATORS[self][0]

    @classmethod
    def from_symbol(cls, char: str) -> Operators | None:
        """ Compares reference symbol with symbol lookup o(n*m) """
        for operator, category in _OPERATORS.items():
            for member in category:
                if member == char:
                    return operator

        return None


_OPERATORS = {
    Operators.MULTIPLICATION: ["*", "x", "·", "∙"],
    Operators.DIVIDED: ["/", "÷"],
    Operators.POWER: [
        "^","⁰","¹","²","³","⁴","⁵",
        "⁶","⁷","⁸","⁹","⁺","⁻",
    ]
}

class Matcher:
    """ matches user defined units in .uiv to qualities """
    @classmethod
    def _construct_unit(cls, unit_str: str) -> Unit:
        """ reconstructs unit from parsed unit string """
        if not unit_str:
            return DIMENSIONLESS

        for op in ["/", "*", "^"]:
            unit_str = unit_str.replace(op, f" {op} ")

        # Tokenizes the unit_str into parts (symbol, operator)
        tokens = unit_str.split()

        if len(tokens) == 1:
            dim = FBase.from_symbol(tokens[0])
            return Unit(Dimension(dim))

        # Initial states of iterators
        result = DIMENSIONLESS
        queue_op = None
        numbers = None

        # Linear iteration - O(n) time complexity
        for token in tokens:
            symbol = FBase.from_symbol(token)
            if not symbol:
                operator = Operators.from_symbol(token)
                if not operator:
                    msg = f"'{token}' is a unknown fundamental unit or operator"
                    raise ValueError(msg)

                # Queues operation and checks for power
                if not queue_op:
                    queue_op = operator
                    break

                msg = f"Failed to run '{queue_op}' before '{operator}'"
                raise RuntimeError(msg)

            # Executes operation on unit pair or fully defined power
            if queue_op:
                if numbers and symbol:
                    # Returns for powers
                    break

                match queue_op:
                    case Operators.MULTIPLICATION:
                        result *= Unit(Dimension(symbol))
                        queue_op = None

                    case Operators.DIVIDED:
                        result /= Unit(Dimension(symbol))
                        queue_op = None

                    case _:
                        msg = f"'{queue_op}' is an unknown operator"
                        raise RuntimeError(msg)

            # if empty result, creates unit
            result = Unit(Dimension(symbol))

        return result

    @classmethod
    def quantity(
        cls, value: Any, prefix: str, unit: str
    ) -> Quantity | str | bool:
        """ Returns a quantity object with those properties """
        if isinstance(value, (str, bool)):
            return value

        # Finds the prefix scale from symbol
        prefix_scale = PrefixScale.from_symbol(prefix)
        if not prefix_scale:
            if prefix:
                msg = f"'{prefix}' is not a prefix symbol"
                raise ValueError(msg)

            # if no prefix scale, set base as scale
            prefix_scale = PrefixScale.BASE

        # Finds / creates the unit
        unit = cls._construct_unit(unit)
        # print(unit)


class Parser:
    """ Parser for .uiv (Unit-Informed Values) files """
    @classmethod
    def _cast(cls, value: str) -> int | float | str | bool | None:
        """ Returns the value with its correct cast """
        try:
            return int(value)
        except ValueError:
            pass

        try:
            return float(value)
        except ValueError:
            pass

        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False

        try:
            return str(value)
        except ValueError:
            pass

        return None

    @classmethod
    def _extract_qualities(cls, value_str: str) -> tuple[Any, str, str]:
        """ Parse .uiv qualities to python objects """
        start = value_str.find('(')
        end = value_str.find(')', start)

        if start != -1 and end != -1:
            unit = value_str[start + 1 : end]

            # Everything before the bracket
            head = value_str[:start].strip()

            if head and not head[-1].isdigit():
                value = head[:-1].strip()
                prefix = head[-1]
            else:
                value = head
                prefix = ""

            return cls._cast(value), cls._cast(prefix), cls._cast(unit)

        return value_str.strip(), "", ""

    @classmethod
    def _section_check(cls, line: str) -> tuple[bool, str | None]:
        """ Finds sections via nested square brackets [section_name] """
        if line.startswith('[') and line.endswith(']'):
            section = line[1:-1]
            return True, section

        return False, None

    @classmethod
    def _skip_comments_lines(cls, line: str) -> bool:
        """ Skips empty lines or comment lines """
        if line.startswith('#') or not line:
            return True
        return False

    @classmethod
    def open(cls, filepath: str) -> str:
        """ import values and their units """
        data: dict = {}
        current_section = None

        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                if cls._skip_comments_lines(line):
                    continue

                status, section = cls._section_check(line)
                if status:
                    current_section = section
                    data[section] = {}
                    continue

                if ':' in line and current_section:
                    key, raw = line.split(':', 1)
                    val, prefix, unit = cls._extract_qualities(raw)
                    Matcher.quantity(val, prefix, unit)
                    data[current_section][key.strip()] = {
                        "value": val,
                        "prefix": prefix,
                        "unit": unit
                    }

        print(data)

Parser.open("examples\parameters.uiv")