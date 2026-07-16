"""
Filename: deserialization.py

Description:
    Type conversion for .ut & .uiv format values.
    Handles lists and nested structures recursively.
    
    Converts strings to Python primitives:
        (int, float, complex, bool, null/none, str).
"""

from __future__ import annotations

from picounits.extensions.utilities.errors import FailedCasting, ParseListFailure


class Deserialize:
    """ Deserialization from text to primitives """
    @classmethod
    def cast(cls, text: str) -> int | float | complex | bool | None | str:
        """ Converts text to python primitives """
        if not isinstance(text, str):
            err = f"Expected str, got {type(text).__name__}"
            raise FailedCasting(text, err)

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
        return str(text)

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

    @classmethod
    def case_list(cls, text: str) -> list:
        """ case list notation Ex. "[1, 2, 3]" -> [1, 2, 3] """
        if not isinstance(text, str):
            err = f"Expected str, got {type(text).__name__}"
            raise FailedCasting(text, err)

        text = text.strip()
        ParseListStructure.valid_list(text)

        # Removes brackets & returns if empty
        text_content = text[1:-1].strip()
        if not text_content: return []

        # Constructs list & returns
        return ParseListStructure.construct_list(text_content)


class ParseListStructure:
    """ Parse embedded list structure """
    @classmethod
    def valid_list(cls, text: str) -> None:
        """ Checks if text is bounded like `[content]` """
        if text.startswith("["):
            if text.endswith("]"):
                return

            msg = f"Malformed nested list (missing closing ']'): {text!r}"
            raise ParseListFailure(cls.__name__, msg)

        msg = f"Expected [item_1,...item_n], got: {text!r}"
        raise ParseListFailure(cls.__name__, msg)

    @classmethod
    def construct_list(cls, content: str) -> list:
        """ Construct list from content via recursively appending lists structures """
        result = []

        # Loop variables
        length = len(content)
        index = 0

        while index < length:
            index = cls._skip_whitespaces(content, index, length)

            # Finds and extract valid section of content
            start = index
            index = cls.tokenizer(content, index, length)
            item_str = content[start:index].strip()

            if not item_str:
                msg = f"Empty element found in list (item at position {start})"
                raise ParseListFailure(cls.__name__, msg)

            # Recursive descent for nested lists
            result.append(cls._recursive_descent(item_str))

            if index < length and content[index] == ',':
                # Skip the comma if stopped on
                index += 1

        return result

    @classmethod
    def _skip_whitespaces(cls, content: str, index: int, length: int) -> int:
        """ Iterates over whitespaces and returns new index """
        while index < length and content[index].isspace():
            index += 1

        return index

    @classmethod
    def tokenizer(cls, content: str, index: int, length: int) -> int:
        """ Finds end of valid section and returns end index """
        depth = 0
        quote_char = None

        while index < length:
            character = content[index]

            if quote_char is None:
                if character in ("'", '"'):
                    quote_char = character
                elif character == '[':
                    depth += 1
                elif character == ']':
                    depth -= 1
                    if depth < 0:
                        msg = f"Unbalanced brackets in {content!r}"
                        raise ParseListFailure(cls.__name__, msg)
                elif character == ',' and depth == 0:
                    break
            else:
                if character == '\\':
                    # Python encodes "\" as "\\" in source code
                    # Ignores any special meaning of the next character.
                    index += 1
                    if index >= length:
                        msg = f"unterminated escape in {content!r}"
                        raise ParseListFailure(cls.__name__, msg)

                elif character == quote_char:
                    quote_char = None

            index += 1

        # Validate at the end of the string
        if quote_char is not None:
            msg = f"Unterminated string in {content!r}"
            raise ParseListFailure(cls.__name__, msg)

        if depth != 0:
            msg = f"Unbalanced brackets in {content!r}"
            raise ParseListFailure(cls.__name__, msg)

        return index

    @classmethod
    def _recursive_descent(cls, content: str) -> list:
        """ Recursive descent for nested lists """
        if content.startswith('['):
            if content.endswith(']'):
                return cls.construct_list(content[1:-1])

            msg = f"Malformed nested list (missing closing ']'): {content!r}"
            raise ParseListFailure(cls.__name__, msg)

        return Deserialize.cast(content)
