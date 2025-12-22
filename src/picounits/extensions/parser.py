"""
Filename: parser.py
Author: William Bowley
Version: 0.1

Description:
    Defines the Parser for .uiv (Unit-Informed Values) files
"""

from typing import Any

from picounits.core.unit import Unit
from picounits.core.qualities import Quantity
from picounits.core.enums import PrefixScale, FBase, Dimension


class Matcher:
    """ matches user defined units in .uiv to qualities """
    @classmethod
    def _preparation(
        cls, value: Any, prefix: str, unit: str
    ) -> tuple[Any, str, str]:
        """ Performs checks and cleans formatting"""
        if not isinstance(prefix, str) or not isinstance(unit, str):
            raise ValueError("Prefix and unit should be strings")

        return value, prefix.lower(), unit.lower()

    @classmethod
    def _construct_unit(cls, unit_str: str):
        """ reconstructs unit from parsed unit string """
        for op in ["/", "*", "^"]:
            unit_str = unit_str.replace(op, f" {op} ")
    
        tokens = unit_str.split()

        result = None
        current_op = "*"

        while idx < len(tokens):
            """ Need to build an operator system for this """

                
    @classmethod
    def quantity(
        cls, value: Any, prefix: str, unit: str
    ) -> Quantity | str | bool:
        """ Returns a quantity object with those properties """
        value, prefix, unit = cls._preparation(value, prefix, unit)

        # Preforms initial check
        if isinstance(value, (str, bool)):
            return value

        # Finds the prefix scale from symbol
        prefix = PrefixScale.from_symbol(prefix)
        cls._construct_unit(unit)


class Parser:
    """ Parser for .uiv (Unit-Informed Values) files """
    @classmethod
    def _cast(cls, value: str) -> int | float | str | bool:
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

        return value

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

# Parser.open("examples\parameters.uiv")