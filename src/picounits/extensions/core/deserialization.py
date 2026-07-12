"""
Filename: deserialization.py

Description:
    Type conversion for .uiv format values.
    Handles lists and nested structures recursively.
    
    Converts strings to Python primitives:
        (int, float, complex, bool, null/none, str).
"""

from __future__ import annotations

from ast import literal_eval
from picounits.extensions.utilities.errors import FailedCasting, DeserializationError, ParseListFailure


class Deserialize:
    """ Deserialization from text to primitives """
    @classmethod
    def cast(cls, text: str) -> int | float | complex | bool | None | str:
        """ Converts text to python primitives """
        text = text.strip()
        if cls.is_quoted(text):
            # Handles quoted strings first
            return str(cls.strip_quotes(text))

        # Try integer value
        try: return int(text)
        except ValueError: pass

        # Try float
        try: return float(text)
        except ValueError: pass

        # Try complex
        try: return complex(text)
        except ValueError: pass

        # Check boolean
        lower = text.lower()
        if lower == "true": return True
        if lower == "false": return False

        # Check null/None
        if text.lower() in ("null", "none"): return None

        # Default to string
        try: return str(text)
        except Exception as err:
            raise FailedCasting(text, err) from err

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

        if text.startswith("'") and text.endswith("'"):
            # Start and end with single quotes
            return True

        return False

    @classmethod
    def strip_quotes(cls, text: str) -> str:
        """ Removes surrounding quotes if present """
        text = text.strip()
        if cls.is_quoted(text):
            # Removes double quotation ref. "{Text}"
            return text[1:-1]

        return text


class ParseListStructure:
    """ Parse embedded list structure """
    @classmethod
    def parse_list(cls, text: str) -> list:
        """ Parse list notation Ex. "[1, 2, 3]" -> [1, 2, 3] """
        text = text.strip()
        _valid_list(text)

        # Removes brackets & returns if empty
        text_content = text[1:-1].strip()
        if not text_content: return []

        # Constructs list & returns
        return _construct_list(text_content)


def _valid_list(text: str) -> None:
    """ Checks if text is bounded like `[content]` """
    if text.startswith("["):
        if text.endswith("]"):
            return

        msg = f"Malformed nested list (missing closing ']'): {text!r}"
        raise ParseListFailure(text, msg)

    msg = f"Expected [item_1,...item_n], got: {text!r}"
    raise ParseListFailure(text, msg)


def _construct_list(content: str) -> list:
    """ Construct list from content via recursively appending lists structures """
    result = []

    # Loop variables
    length = len(content)
    index = 0
    depth = 0
    while index < length:
        _skip_whitespaces(content, index, length)

        # Finds and extract valid section of content
        start = index
        index, depth, quoted_char = _list_section(content, index, length)
        item_str = content[start:index].strip()

        if not item_str and index < length and content[index-1] == ",":
            # Ignores if last item is empty
            continue

        if not item_str:
            msg = f"Empty element found in list {item_str!r}"
            fix = "(possible stray common or malformed idea)"
            raise ParseListFailure(content, f"{msg} | {fix}")

        # Recursive descent for nested lists
        result.append(_recursive_descent(item_str))

        if index < length and content[index] == ',':
            # Skip the comma if stopped on
            index += 1

    if depth != 0:
        msg = f"Unbalanced brackets in {content!r}"
        raise ParseListFailure(content, msg)

    if quoted_char is not None:
        msg = f"Unterminated string in {content!r}"
        raise ParseListFailure(content, msg)

    return result


def _skip_whitespaces(content: str, index: int, length: int) -> int:
    """ Iterates over whitespaces and returns new index """
    while index < length and content[index].isspace():
        index += 1

    return index


def _list_section(content: str, index: int, length: int) -> tuple[int, int, str]:
    """ Finds end of valid section and returns depth & quoted_char """
    depth = 0
    quote_char = None

    while index < length:
        character = content[index]

        if quote_char is None:
            depth, quote_char = _list_depth(character, quote_char, depth)

            if depth < 0:
                msg = f"Unbalanced brackets in {content!r}"
                raise DeserializationError("list_slicer", msg)

            if character == ',' and depth == 0:
                break

        else:
            if character == '\\':
                # Python encodes "\" as "\\" in source code
                # Ignores any special meaning of the next character.
                index += 1
                if index >= length:
                    msg = f"unterminated escape in {content!r}"
                    raise ParseListFailure(content, msg)

            elif character == quote_char:
                quote_char = None

        index += 1

    return index, depth, quote_char


def _list_depth(char: str, quote_char: str, depth: int) -> tuple[int, str]:
    """ Evaluates the depth of the current list structure """
    # If the character is either a double or single quote
    if char == '"' or char == "'": quote_char = char

    # If the character is a open bracket, increase depth
    if char == '[': depth += 1

    # If the charger is a close bracket, decrease depth
    if char == ']': depth -= 1
    return depth, quote_char


def _recursive_descent(content: str) -> list:
    """ Recursive descent for nested lists """
    if content.startswith('['):
        if content.endswith(']'):
            return _construct_list(content)

        msg = f"Malformed nested list (missing closing ']'): {content!r}"
        raise ParseListFailure(content, msg)

    return Deserialize.cast(content)
