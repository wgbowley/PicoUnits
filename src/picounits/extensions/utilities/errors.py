"""
Filename: parser_errors.py

Description:
    Defines the parser errors classes to 
    ensure descriptive error messages are
    returned to the user
"""

from typing import Any

# Generic Errors
class ParserError(ValueError):
    """ Exception for Parser errors when parsing """
    def __init__(self, caller: str, error: str):
        """ Returns a custom error message """
        msg = f"'{caller}' raised error: {error}. "
        super().__init__(msg)


class DeserializationError(ValueError):
    """ Exception for Deserializer errors when parsing """
    def __init__(self, caller: str, error: str):
        """ Returns a custom error message """
        msg = f"'{caller}' raised error: {error}. "
        super().__init__(msg)



# Specific errors
class UnknownOperator(ValueError):
    """ Exception for unknown operator during construction """
    def __init__(self, char: str, operator: str):
        """ Returns a custom error message """
        msg = f"{char!r} is an unknown operator. Supported operators are {operator!r}"
        super().__init__(msg)


class AmbiguousPower(ValueError):
    """ Exception for ambiguous power syntax """
    def __init__(self, error: str):
        """ Returns an ambiguous power error """
        msg = f"Ambiguous power syntax: {error!r}"
        super().__init__(msg)


class FailedCasting(ValueError):
    """ Exception for failure during casting """
    def __init__(self, text: Any, error: str):
        """ Returns a failed casting error """
        msg = f"Failed to cast {text!r} as python primitive, error: {error!r}"
        super().__init__(msg)


class ParseListFailure(ValueError):
    """ Exception for failure of parsing lists """
    def __init__(self, text: Any, msg: str):
        """ Returns a failed casting error """
        msg = f"Failed to parse {text!r} as list, {msg}"
        super().__init__(msg)
