"""
Filename: syntax.py

Description:
    syntax for .ut & .uiv formats.
    
    Handles line parsing, value: prefix(unit) pair
    and bracket matching
"""

from __future__ import annotations

from typing import Any
from dataclasses import dataclass

from picounits.extensions.utilities.errors import UnbalancedDepth, ParserError
from picounits.extensions.core.deserialization import Deserialize


@dataclass
class ExtractionState:
    """ Stores the state of the extractor during extraction """
    index: int = 0
    break_index: int = 0
    depth: int = 0
    quote_char: str | None = None
    content: list[str] | None = None

    def distinguished_character(self, character: str) -> None:
        """ Distinguishes between inside & outside quotes """
        if character in ("'", '"'):
            # Distinguishes between inside & outside quotes
            if not self.quote_char:
                self.quote_char = character
                return

            if character == self.quote_char:
                self.quote_char = None
                return

    def is_escaped(self, line: str) -> bool:
        """ Check if character at index is escaped. """
        # Python encodes "\" as "\\" in source code
        return self.index > 0 and line[self.index-1] == '\\'


class ExtractPairs:
    """ Initial syntax parsing for the .ut & .uiv formats """
    @classmethod
    def extract_key_value(cls, line: str) -> tuple[str, str] | None:
        """ Split line on opened colon (quantity_name: value prefix(unit))"""
        # Initializes the extractor state
        state = ExtractionState()

        # Remove inline comments first
        for comment_char in ('#', ';'):
            if comment_char in line:
                line = line[:line.index(comment_char)].rstrip()

        for index, character in enumerate(line):
            state.index = index

            if state.is_escaped(line):
                # Handles escaped characters via aborting to next iteration
                continue

            # Handles quoted strings
            state.distinguished_character(character)

            if character == ":" and not state.quote_char:
                # Returns the quality name & quality value strings
                # Also removes leading/trailing whitespace using .strip()
                return line[:index].strip(), line[index+1:].strip()

        return None


class ExtractBrackets:
    """ Extract content between matching brackets """
    @classmethod
    def extract_content(cls, line: str) -> tuple[str, int] | None:
        """ Extracts content between matching brackets """
        open_bracket_index = line.find('[')

        if open_bracket_index == -1:
            # Handles when no open_bracket is found inline
            return None

        return cls._bracket_syntaxes(line, open_bracket_index)

    @classmethod
    def _bracket_syntaxes(cls, line: str, open_index: int) -> tuple[str, int] | None:
        """ Stateful parser for extracting bracketed content """
        # Initializes the extractor state
        state = ExtractionState()

        for index in range(open_index, len(line)):
            character = line[index]
            state.index = index

            if state.is_escaped(line):
                # Handles escaped characters via aborting to next iteration
                continue

            # Handles quoted strings & skips depth if inside quotes
            state.distinguished_character(character)
            if state.quote_char: continue

            # Updates depth based on open & closed brackets
            if character == '[':
                state.depth += 1

            elif character == ']':
                state.depth -= 1
                if state.depth == 0:
                    # Returns content once end bracket is found
                    return line[open_index+1:index], index

        raise UnbalancedDepth(cls.__name__, line, "[ ]")


class ExtractParentheses:
    """ Extract content between matching parentheses """
    @classmethod
    def extract_content(cls, line: str) -> list[str]:
        """ Extracts parenthesized content from line """
        # Initializes the parser state dataclass
        state = ExtractionState()
        state.content = []

        length = len(line)
        while state.index < len(line):
            # Skips non-parenthesized & if index is greater than length, breaks loop
            state.index = cls.skip_non_parentheses(line, state.index)
            if state.index >= length: break

            # Resets variables & extract inner content
            state.depth = 1
            state.index += 1
            state.break_index = state.index
            state.quote_char = None

            cls._extract_content(line, state, length)

            # Raises unbalanced depth error if missing end parentheses
            if state.depth > 0: raise UnbalancedDepth(cls.__name__, line, "( )")

        return state.content

    @classmethod
    def skip_non_parentheses(cls, line: str, start: int) -> int:
        """ Skips non parenthesized characters """
        position = line.find('(', start)

        # Handles when no open parentheses is found inline
        if position == -1: return len(line)
        return position

    @classmethod
    def _extract_content(cls, line: str, state: ExtractionState, length: int) -> None:
        """ Extract content inside parenthesized group """
        while state.index < length and state.depth > 0:
            character = line[state.index]

            if state.is_escaped(line):
                # Handles escaped characters via aborting to next iteration
                state.index += 1
                continue

            # Handles quoted strings & skips depth if inside quotes
            state.distinguished_character(character)

            # Handles unquoted parenthesis
            if not state.quote_char:
                # Handles parenthesis depth
                if character == '(':
                    state.depth += 1

                elif character == ')':
                    state.depth -=1
                    if state.depth == 0:
                        # Found matching closing parenthesis
                        state.content.append(line[state.break_index:state.index])
                        state.index += 1
                        return

            state.index += 1


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
            # If string is quoted return value without prefix and unit
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
        list_result = Deserialize.case_list(f"[{content}]")

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
                remainder = before[:-1].rstrip()

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
        split_prefix_unit = line[:paren_index]
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
