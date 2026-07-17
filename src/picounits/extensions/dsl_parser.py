"""
Filename: dsl_parser.py

Description:
    Domain specific language parser for .ut (unit types)
    & .uiv (unit informed values).
    
    Orchestrates deserialization, syntax analysis & 
    construction of units
"""


from pathlib import Path
from typing import IO, Any

from picounits.core.unit import Unit
from picounits.extensions.attribute_loader import DynamicLoader
from picounits.extensions.utilities.errors import ParserError

from picounits.extensions.core.deserialization import Deserialize
from picounits.extensions.core.syntax import ExtractParentheses, ExtractBrackets


class Parser:
    """ Parser for .ut & .uiv file formats"""
    @classmethod
    def open(
        cls, filepath: Path | str | IO | Any, derived: Path | str | IO | Any = None
    ) -> DynamicLoader:
        """ Parses .uiv file into an attribute tree structure """
        _, _ = filepath, derived
        return

    @classmethod
    def import_derived(cls, filepath: Path | str | IO | Any) -> dict[str, Unit]:
        """ Parses .ut file and interprets unit strings into runtime registry """
        _ = filepath
        return


class QualityExtraction:
    """ Extracts value, prefix and unit from line """
    @classmethod
    def extract(cls, text: str) -> tuple[Any, str | list, str | list]:
        """ Extracts value, prefix and unit from line. """
        if not isinstance(text, str):
            err = f"Expected str, got {type(text).__name__}"
            raise ParserError(cls.__name__, err)

        # Removes leading and trailing whitespaces
        text = text.strip()
        if Deserialize.is_quoted(text):
            # If string is quoted return vale without prefix and unit
            return Deserialize.strip_quotes(text), "", ""

        if text.startswith('['):
            # If text starts with `square brackets`, its interpreted as a list
            return cls._from_list_structure(text)

        # Single values with potential unit
        parentheses_content = ExtractParentheses.extract_content(text)
        if parentheses_content:
            return cls._from_parentheses(text, parentheses_content)

        # Assumed plain text without prefix or unit
        return (Deserialize.cast(text), "", "")

    @classmethod
    def _from_list_structure(cls, text: str) -> tuple[Any, str | list, str | list] | None:
        """ Extracts qualities from list structure. """
        # Extracts content from between brackets
        bracket_content = ExtractBrackets.extract_content(text)
        if not bracket_content:
            msg = f"Invalid list structure: {text!r}"
            raise ParserError(cls.__name__, msg)

        # Splits content and end index
        content, end_index = bracket_content
        list_result = Deserialize.case_list(content)

        # Extracts unit strings and removes leading/trailing whitespaces
        unit_strings = text[end_index + 1:].strip()
        if unit_strings:
            units = ExtractParentheses.extract_content(unit_strings)
            num_units = len(units)

            if num_units > 1:
                prefixes = cls._column_wise_prefixes(unit_strings)
                return list_result, prefixes, units

            elif num_units == 1:
                prefix = cls._list_prefix_extraction(unit_strings)
                return list_result, prefix, units

        # Assumed plain list without prefix or unit
        return list_result, "", ""

    @classmethod
    def _column_wise_prefixes(cls, unit_strings: str) -> list[str]:
        """ Extracts prefixes to for column wise prefixes """
        prefixes = []

        # Finds prefix at "prefix(unit)" boundary and selects everything before unit
        for item in unit_strings.split(','):
            parentheses_index = item.find('(')
            prefix = item[:parentheses_index].strip()
            prefixes.append(prefix)

        return prefixes

    @classmethod
    def _list_prefix_extraction(cls, unit_strings: str) -> list[str] | str:
        """ Extracts prefixes to append to single unit """
        last_open_parentheses_index = unit_strings.rfind('(')

        if last_open_parentheses_index > 0:
            # Removes the trailing whitespaces
            before = unit_strings[:last_open_parentheses_index].rstrip()

            # if before is not none and last item is alphabetic
            if before and before[-1].isalpha():
                # Removes the trailing whitespaces
                remainder = before[:-1].rstrip
                if not remainder or remainder[-1] in ',)':
                    return before[-1]

        msg = f"Invalid prefixes/unit structure: {unit_strings!r}"
        raise ParserError(cls.__name__, msg)

    @classmethod
    def _from_parentheses(
        cls, line: str, content: str | list[str]
    ) -> tuple[Any, str | list, str | list]:
        """ Extracts qualities from parentheses content """
        # Discovers where the prefix and unit boundary exists
        paren_index = ExtractParentheses.skip_non_parentheses(line, 0)

        # Splits along the "prefix(unit)" boundary and selects the first item as unit
        split_prefix_unit = line[:paren_index].strip()
        unit = content[0]

        if split_prefix_unit:
            # Checks item in-front of unit for prefix
            if not (split_prefix_unit[-1].isdigit and split_prefix_unit.endswith('.')):
                # If the prefix is not a digit and also not a dot than returns value, prefix, unit
                value = split_prefix_unit[:-1].strip()
                prefix = split_prefix_unit[-1]

                return (Deserialize.cast(value), prefix, unit)

            # If split_prefix is none than return value with empty prefix
            return (Deserialize.cast(split_prefix_unit), "", unit)

        msg = f"Invalid parentheses structure: {line!r}"
        raise ParserError(cls.__name__, msg)
