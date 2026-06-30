"""
Filename: parser_errors.py

Description:
    Holds the parser error class to ensure
    no circular imports occur during runtime.
"""

from typing import Any

class ParserError(ValueError):
    """ Exception for parser errors when parsing """
    def __init__(self, caller: str, error: str):
        """ Returns a custom error message """
        msg = f"'{caller}' raised error: {error}. "
        super().__init__(msg)


class AttributeNotFound(AttributeError):
    """ Exception for attribute not found error """
    def __init__(self, attribute: str, path: str):
        """ Returns a custom error message """
        self.path = path
        self.attribute = attribute

        msg = f"'{attribute}' not found at '{path}' within loader tree"
        super().__init__(msg)


class InjectionError(Exception):
    """Raised when a value cannot be injected into a Loader tree."""
    def __init__(self, path: str, value: Any):
        self.path = path
        self.value = value

        msg = f"Failed to inject '{value}' at '{path}'"
        super().__init__(msg)
