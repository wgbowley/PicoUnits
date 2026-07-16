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


class ParseListFailure(ValueError):
    """ Exception for failure of parsing lists """
    def __init__(self, caller: Any, msg: str):
        """ Returns a failed casting error """
        msg = f"'{caller}' raised error: {msg}. "
        super().__init__(msg)


# Specific errors
class UnknownOperator(ValueError):
    """ Exception for unknown operator during construction """
    def __init__(self, char: str, operator: str):
        """ Returns a custom error message """
        msg = f"{char!r} is an unknown operator. Supported operators are {operator!r}"
        super().__init__(msg)


class UnknownPrefix(ValueError):
    """ Exception for unknown prefix during construction """
    def __init__(self, char: str, prefixes: str):
        """ Returns a custom error message """
        msg = f"{char!r} is an prefix. Supported prefix are {prefixes!r}"
        super().__init__(msg)


class FailedCasting(ValueError):
    """ Exception for failure during casting """
    def __init__(self, text: Any, error: str):
        """ Returns a failed casting error """
        msg = f"Failed to cast {text!r} as python primitive, error: {error!r}"
        super().__init__(msg)


class ColumnAttribute(AttributeError):
    """ Exception for column attribute out of range"""
    def __init__(self, attribute_type: Any):
        """ Returns a column attribute error """
        msg = f"Failed to construct nested array due to {attribute_type!r} out of range"
        super().__init__(msg)


class UnsupportedType(ValueError):
    """ Exception for unsupported type during unit construction"""
    def __init__(self, value_type: Any):
        """ Returns a column attribute error """
        msg = f"Failed to construct unit due to unsupported type: {value_type!r}"
        super().__init__(msg)
