"""
Filename: converter.py
Author: William Bowley
Version: 0.2

Description:
    Type conversion for .uiv format values.
    Converts strings to Python primitives (int, float, bool, str).
    Handles lists and nested structures recursively.
"""

from __future__ import annotations
from typing import Any

from picounits.extensions.parser_errors import ParserError
from picounits.extensions.utilities.tokenizer import Tokenizer


class Converter:
    """ Type conversion utilities for parsing """
    @classmethod
    def cast(cls, text: Any) -> int | float | str | bool | None:
        """ Converts text to appropriate python type """
        text = text.strip()
        if Tokenizer.is_quoted(text):
            # Handles quoted strings first
            return Tokenizer.strip_quotes(text)

        # Try integer
        try:
            return int(text)
        except ValueError:
            pass

        # Try float
        try:
            return float(text)
        except ValueError:
            pass
        
        # Try complex
        try:
            return complex(text)
        except ValueError:
            pass

        # Check boolean
        lower = text.lower()
        if lower == "true":
            return True
        elif lower == "false":
            return False

        # Check null/None
        if text.lower() in ("null", "none"):
            return None

        # Default to string
        try:
            return str(text)
        except ValueError:
            msg = f"Failed to cast '{text}' as str, bool, int or float"
            raise ParserError(cls.__name__, msg) from None

    @classmethod
    def parse_list(cls, list_str: str) -> list:
        """ Recursively parse list notation Ex. "[1, 2, 3]" -> [1, 2, 3]"""
        list_str = list_str.strip()

        if not (list_str.startswith("[") and list_str.endswith("]")):
            msg = f"Expected [...] list, got: {list_str}"
            raise ParserError(cls.__name__, msg)

        # Extract list content "[1, 2, 3]" -> "1, 2, 3"
        list_content = list_str[1:-1].strip()

        if not list_content:
            return []

        result = []
        index = 0
        length = len(list_content)
        depth = 0

        while index < length:
            # Skip whitespaces
            while index < length and list_content[index].isspace():
                index += 1

            # Start of next element
            start = index
            depth = 0
            quote_character = None

            while index < length:
                character = list_content[index]

                if quote_character is None:
                    # outside string

                    if character in '"\'':
                        quote_character = character
                    elif character == '[':
                        depth += 1
                    elif character == ']':
                        depth -= 1
                        if depth < 0:
                            msg = f"Unbalanced brackets in {list_str!r}"
                            raise ParserError(cls.__name__, msg)

                    elif character == ',' and depth == 0:
                        break   # end of item
                else:
                    # inside string
                    if character == '\\':
                        # skip escaped character
                        index += 1
                        if index >= length:
                            msg = f"Unterminated escape in {list_str!r}"
                            raise ParserError(cls.__name__, msg)

                    elif character == quote_character:
                        quote_character = None

                index += 1

            # Extract the slice
            item_str = list_content[start:index].strip()

            if not item_str and index < length and list_content[index-1] == ',':
                # Trailing comma & empty last item -> ignore if empty
                continue

            if not item_str:
                msg = (
                    f"Empty element found in list {list_str!r} "
                    "(possible stray comma or malformed item)"
                )
                raise ParserError(cls.__name__, msg)

            # Recursive descent for nested lists
            if item_str.startswith('['):
                if not item_str.endswith(']'):
                    msg = f"Malformed nested list (missing closing ']'): {item_str!r}"
                    raise ParserError(cls.__name__, msg)

                result.append(cls.parse_list(item_str))
            else:
                result.append(cls.cast(item_str))

            # Skip the comma we stopped on
            if index < length and list_content[index] == ',':
                index += 1

        if depth != 0:
            msg = f"Unbalanced brackets in {list_str!r}"
            raise ParserError(cls.__name__, msg)

        if quote_character is not None:
            msg = f"Unterminated string in {list_str!r}"
            raise ParserError(cls.__name__, msg)

        return result
