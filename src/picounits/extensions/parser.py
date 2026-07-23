"""
Filename: dsl_parser.py

Description:
    Domain specific language parser for .ut (unit types)
    & .uiv (unit informed values).
    
    Orchestrates deserialization, syntax analysis & 
    construction of units
"""


from __future__ import annotations

from pathlib import Path
from typing import IO, Any

from picounits.configuration.management import add_derived_units

from picounits.extensions.loader import DynamicLoader
from picounits.extensions.core.syntax import ExtractPairs, QualityExtraction
from picounits.extensions.core.construction import ConstructQuantity, ConstructUnits

from picounits.extensions.utilities.errors import ParserError, BackCompatibilityWarning


class Parser:
    """ Parser for .ut & .uiv file formats"""
    @classmethod
    def open(
        cls, filepath: Path | str | IO | Any, derived: Path | str | IO | Any = None
    ) -> DynamicLoader:
        """ Parses .uiv file into an attribute tree structure """
        if derived:
            # Imports derived units if available
            cls.import_derived(derived)

        # Checks file type and reads lines into memory
        if isinstance(filepath, (str, Path)):
            path = Path(filepath)
            if path.suffix.lower() != '.uiv':
                raise ValueError(f"Expected .uiv file, got {path.suffix}")

        lines = cls._read_lines(filepath)

        # Parses lines into dynamic loader
        data = ParseLines.parse(lines, filepath)
        return DynamicLoader(data)

    @classmethod
    def import_derived(cls, filepath: Path | str | IO | Any) -> None:
        """ Parses .ut file and interprets unit strings into runtime registry """
        # Checks file type and read lines into memory
        derived_path = Path(filepath)
        if derived_path.suffix.lower() != '.ut':
            raise ValueError(f"Expected .ut file, got {derived_path.suffix}")

        lines = cls._read_lines(filepath)

        # State & derived unit dictionary
        status = False
        registry = {}

        # Constructs a registry of derived units
        for line in lines:
            if ParseLines.skip_comment(line):
                # Skips comments and empty lines
                continue

            # Splits the key and the value pairs into two strings
            result = ExtractPairs.extract_key_value(line)
            if not result:
                # If no key value pairs are extracted
                continue

            # Decomposes result into symbol & units
            symbol, unit_str = result
            if symbol.lower() == "format":
                # Updates the format state variable
                status = True
                continue

            # Constructs the unit
            registry[symbol] = ConstructUnits.construct_unit(unit_str)

        if not status:
            # Raises warning for missing 'format' key in version
            BackCompatibilityWarning(filepath).display()

        return add_derived_units(registry)

    @staticmethod
    def _read_lines(filepath_or_file: Path | str | IO | Any) ->  list[str]:
        """Read lines from file path or file-like object."""
        if hasattr(filepath_or_file, 'read') and hasattr(filepath_or_file, 'readlines'):
            # Check if it's a file-like object
            return filepath_or_file.readlines()

        # Convert to Path and validate
        filepath = Path(filepath_or_file)
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        with filepath.open('r', encoding='utf-8') as f:
            return f.readlines()


class ParseLineState:
    """Stores the state of the line parser"""
    index: int = 0
    status: bool = False
    format_status: bool = False
    section: str | None = None
    content: dict | None = None


class ParseLines:
    """ Parse lines for .ut & .uiv files formats """
    @classmethod
    def parse(cls, lines: list[str], filepath: Path | str | IO | Any) -> dict:
        """ Parses and extracts logic from raw text into qualities """
        # Initializes the parser state
        state = ParseLineState()
        state.content = {}

        while state.index < len(lines):
            line = lines[state.index].strip()
            state.index += 1

            if cls.skip_comment(line):
                # Skips comments and empty lines
                continue

            is_section, name = cls._is_section(line)
            if is_section:
                # Updates section based if identified
                state.section = name
                state.content[name] = {}

                # Updates compatibility
                state.status = False
                if name.lower() == "version": state.status = True
                continue

            # Attempts to parse key-value pair
            split_result = ExtractPairs.extract_key_value(line)
            if not split_result: continue

            if state.section is None:
                # Key-value pair found outside a parent section
                msg = f"key-value pair outside section {line!r}"
                raise ParserError(cls.__name__, msg)

            key, raw_value = split_result
            if raw_value.startswith('['):
                # Handles multi-line values (lists that span multiple lines)
                raw_value = cls._handle_multi_line(state, lines, raw_value)

            # Checks for format section
            if state.status:
                if key.lower() == "format":
                    # If format is found within the [version] section
                    state.format_status = True

            # Extracts value, prefix and unit
            value, prefix, unit = QualityExtraction.extract(raw_value)

            # Constructs array of quantity (value_1: unit_1, ..., value_n: unit_n)
            if isinstance(unit, list) and isinstance(value, list):
                if all(isinstance(entry, (complex, int, float)) for entry in value):
                    # If all values are complex, int or float than construct array
                    array = []
                    for idx, val in enumerate(value):
                        quantity = ConstructQuantity.quantity(val, prefix[idx], unit[idx])
                        array.append(quantity)

                    state.content[state.section][key] = array
                    continue

            # Construct the quantity (Arrays, single value unit pairs)
            quantity = ConstructQuantity.quantity(value, prefix, unit)
            state.content[state.section][key] = quantity

        if not state.format_status:
            # Raises warning for missing 'format' key in version
            BackCompatibilityWarning(filepath).display()

        return state.content

    @classmethod
    def skip_comment(cls, line: str) -> bool:
        """ Check if line should be skipped (empty or comment) """
        line = line.strip()

        # Returns the result as a boolean
        return not line or line.startswith('#')

    @classmethod
    def _handle_multi_line(cls, state: ParseLineState, lines: list[str], raw_value: str) -> str:
        """ Handles multi-line values such as lists """
        open_count, close_count = cls._count_brackets(raw_value)

        # Collects lines until balanced
        while open_count > close_count and state.index < len(lines):
            # Removes whitespaces and adds next_line
            next_line = lines[state.index].strip()
            state.index += 1
            raw_value += ' ' + next_line

            # Finds next open and close bracket and iterates values
            next_open, next_close = cls._count_brackets(next_line)
            open_count += next_open
            close_count += next_close

        return raw_value

    @classmethod
    def _count_brackets(cls, text: str) -> tuple[int, int]:
        """ Count opening and closing brackets """
        return text.count('['), text.count(']')

    @classmethod
    def _is_section(cls, line: str) -> tuple[bool, str]:
        """ Check if line defines a section [name] """
        line = line.strip()
        if line.startswith('[') and line.endswith(']'):
            # Returns the contents if true
            return True, line[1:-1]

        # Returns a empty string if false
        return False, ""
