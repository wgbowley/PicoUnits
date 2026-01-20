"""
Filename: tokenizer.py
Author: William Bowley
Version: 0.1

Description:
    Low-level tokenization for .uiv format.
    Handles string parsing, bracket matching,
    delimiter splitting.
"""

from __future__ import annotations
from picounits.extensions.parser_errors import ParserError

class Tokenizer:
    """ Stateless tokenization utilities for parsing """

    @classmethod
    def is_quoted(cls, text: str) -> bool:
        """ Check if text is surrounded by quotes """
        text = text.strip()

        if len(text) < 2:
            # Empty quoted text Ex. ("")
            return False

        if text.startswith('"') and text.endswith('"'):
            # Start and end with double quotes
            return True

        elif text.startswith("'") and text.endswith("'"):
            # Start and end with single quotes
            return True

        return False

    @classmethod
    def strip_quotes(cls, text: str) -> str:
        """ Removes surrounding quotes if present """
        text = text.strip()
        if cls.is_quoted(text):
            # Removes double quotation
            return text[1:-1]
        return text

    @classmethod
    def count_brackets(cls, text: str) -> tuple[int, int]:
        """ Count opening and closing brackets """
        return text.count('['), text.count(']')

    @classmethod
    def split_key_value_pairs(cls, line: str) -> tuple[str, str] | None:
        """ Split line on first unquoted colon Ex. speed: 10 M(ms^-1)"""
        quote_character = None

        for index, character in enumerate(line):
            # Handles if character is escaped
            if index > 0 and line[index-1] == '\\':
                continue

            # Handles ':' inside quotation via toggle logic
            if character in "\"'":
                # Ex. "Hello" true inside 'hello' empty outside.
                if not quote_character:
                    quote_character = character
                elif character == quote_character:
                    quote_character = None

            elif character == ':' and not quote_character:
                return line[:index], line[index+1:].strip()

        return None

    @classmethod
    def extract_bracket_content(
        cls, text: str, start_index: int = 0
    ) -> tuple[str, int] | None:
        """
        Extracts content between matching brackets Ex. '[1,2,3]' -> (1,2,3)
        """
        open_index = text.find('[', start_index)

        if open_index == -1:
            # Handles when '[' is not founded
            return None

        bracket_pair_depth = 0
        quote_character = None
        for index in range(open_index, len(text)):
            character = text[index]

            # Handles if character is escaped
            if index > open_index and text[index-1] == '\\':
                continue

            # Handles brackets inside quotes
            if character in "\"'":
                # Ex. "Hello" true inside 'hello' empty outside.
                if not quote_character:
                    quote_character = character
                elif character == quote_character:
                    quote_character = None

            # skip bracket depth check if inside quotes
            if quote_character:
                continue

            if text[index] == '[':
                bracket_pair_depth += 1

            elif text[index] == ']':
                bracket_pair_depth -= 1
                if bracket_pair_depth == 0:
                    # Found matching brackets
                    content = text[open_index + 1:index]
                    return content, index

        msg = f"'{text}' requires balanced brackets to be parsed."
        raise ParserError(cls.__name__, msg)

    @classmethod
    def extract_parent_groups(cls, text: str) -> list[str]:
        """ Extracts all top-level parenthesized groups """
        groups = []
        index = 0
        MAX_ITERATIONS = 10000
        iterations = 0

        while index < len(text):
            iterations += 1
            if iterations > MAX_ITERATIONS:
                msg = f"Loop limit exceeded in: {text[:50]}..."
                raise ParserError(cls.__name__, msg)

            # Handles whitespace/delimiters via skipping
            if text[index] not in '(':
                index += 1
                continue

            # Start tracking the group
            start = index + 1
            depth = 0
            quote_character = None
            found_match = False  

            # Internal state machine
            while index < len(text):
                character = text[index]

                # Handles if character is escaped
                if index > 0 and text[index-1] == '\\':
                    continue

                # Handles brackets inside quotes
                if character in "\"'":
                    # Ex. "Hello" true inside 'hello' empty outside.
                    if not quote_character:
                        quote_character = character
                    elif character == quote_character:
                        quote_character = None

                # Handles parens (only if not in quotes)
                if not quote_character:
                    if character == '(':
                        depth += 1
                    elif character == ')':
                        depth -= 1
                        if depth == 0:
                            groups.append(text[start:index])
                            found_match = True
                            index += 1
                            break

                index += 1

            # Check if the inner loop fails to find a closing paren
            if not found_match:
                msg = f"Unbalanced parentheses in: {text}"
                raise ParserError(cls.__name__, msg)
