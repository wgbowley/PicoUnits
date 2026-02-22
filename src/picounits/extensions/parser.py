"""
Filename: parser.py
Author: William Bowley
Version: 0.2

Description:
    High-level parser for .uiv (Unit-Informed Values) files.
    Orchestrates tokenization, conversion, and construction.
"""

from __future__ import annotations
from typing import Any

from picounits.extensions.utilities.tokenizer import Tokenizer
from picounits.extensions.utilities.construction import Construct
from picounits.extensions.utilities.converter import Converter
from picounits.extensions.parser_errors import ParserError

from picounits.extensions.loader import DynamicLoader
from picounits.core.unit import Unit

class Parser:
    """ Parser for .uiv (unit informed values) file format """

    @classmethod
    def _is_section(cls, line: str) -> tuple[bool, str | None]:
        """ Check if line defines a section [name] """
        line = line.strip()
        if line.startswith('[') and line.endswith(']'):
            return True, line[1:-1]

        return False, None

    @classmethod
    def _should_skip(cls, line: str) -> bool:
        """ Check if line should be skipped (empty or comment) """
        line = line.strip()
        return not line or line.startswith('#')

    @classmethod
    def _extract_qualities(
        cls, value_str: str
    ) -> tuple[Any, str | list, str | list]:
        """ Extracts value, prefix and unit from raw string. """
        value_str = value_str.strip()

        # Check for quoted string
        if Tokenizer.is_quoted(value_str):
            return Tokenizer.strip_quotes(value_str), "", ""

        # Check for list structure
        if value_str.startswith('['):
            bracket_result = Tokenizer.extract_bracket_content(value_str, 0)
            if not bracket_result:
                msg = f"Invalid list structure: {value_str!r}"
                raise ParserError(cls.__name__, msg)

            content, end_index = bracket_result
            list_value = Converter.parse_list(f"[{content}]")
            remainder = value_str[end_index + 1:].strip()

            if remainder:
                # Extract unit specifications
                units = Tokenizer.extract_paren_groups(remainder)

                if len(units) > 1:
                    # Multiple units (column-wise)

                    """ TODO: Add support for per-column prefixes """

                    prefixes = [""] * len(units)
                    return list_value, prefixes, units

                elif len(units) == 1:
                    # Single unit with potential prefix
                    unit = units[0]

                    # Check for prefix before unit
                    last_paren = remainder.rfind('(')
                    if last_paren > 0:
                        before = remainder[:last_paren].rstrip()

                        if before and before[-1].isalpha():
                            rest = before[:-1].rstrip()

                            if not rest or rest[-1] in ',)':
                                return list_value, before[-1], unit

                    return list_value, "", unit

            return list_value, "", ""

        # Single value with potential unit
        paren_groups = Tokenizer.extract_paren_groups(value_str)

        if paren_groups:
            # Find where unit starts
            paren_idx = value_str.find('(')
            head = value_str[:paren_idx].strip()
            unit = paren_groups[0]

            # Check for prefix (single letter before unit, not part of number)
            if head and not head[-1].isdigit() and not head.endswith('.'):
                value = head[:-1].strip()
                prefix = head[-1]
            else:
                value = head
                prefix = ""

            return Converter.cast(value), prefix, unit

        # Just a plain value with no unit
        return Converter.cast(value_str), "", ""

    @classmethod
    def _parse_lines(cls, lines: list[str]) -> dict:
        """ Extract logic from raw_open into reusable method """
        data = {}
        current_section = None

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            i += 1

            # Skip comments and empty lines
            if cls._should_skip(line):
                continue

            # Check for section
            is_section, section_name = cls._is_section(line)
            if is_section:
                current_section = section_name
                data[section_name] = {}
                continue

            # Parse key-value pair
            split_result = Tokenizer.split_key_value_pairs(line)
            if not split_result:
                continue

            if current_section is None:
                msg = f"Key-value pair outside section: {line!r}"
                raise ParserError(cls.__name__, msg)

            key, raw_value = split_result

            # Handle multi-line values (lists that span multiple lines)
            if raw_value.startswith('['):
                open_count, close_count = Tokenizer.count_brackets(raw_value)

                # Collect lines until balanced
                while open_count > close_count and i < len(lines):
                    next_line = lines[i].strip()
                    i += 1
                    raw_value += ' ' + next_line

                    next_open, next_close = Tokenizer.count_brackets(next_line)
                    open_count += next_open
                    close_count += next_close

            # Extract value, prefix, and unit
            value, prefix, unit = cls._extract_qualities(raw_value)

            # Construct the quantity
            quantity = Construct.quantity(value, prefix, unit)
            data[current_section][key] = quantity

        return data

    @classmethod
    def open(cls, filepath_or_file, loader_class=None) -> DynamicLoader:
        """ Parse .uiv file into structured data via attribute injection. """
        if loader_class is None:
            loader_class = DynamicLoader

        # If it's a file-like object, read lines directly
        if hasattr(filepath_or_file, "read"):
            lines = filepath_or_file.readlines()
            return loader_class(cls._parse_lines(lines))

        else:
            with open(filepath_or_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                return loader_class(cls._parse_lines(lines))

    @classmethod
    def open_derived(cls, filepath) -> dict[str, Unit]:
        """ Parses a units.uiv file into a symbol -> Unit registry """
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        registry = {}
        for line in lines:
            result = Tokenizer.split_key_value_pairs(line.strip())
            if not result:
                continue
            symbol, unit_str = result
            registry[symbol] = Construct.tokenize_unit(unit_str)

        return registry
