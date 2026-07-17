"""
Filename: syntax.py

Description:
    syntax for .ut & .uiv formats.
    
    Handles line parsing, value: prefix(unit) pair
    and bracket matching
"""

from __future__ import annotations
from dataclasses import dataclass

from picounits.extensions.utilities.errors import UnbalancedDepth

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
