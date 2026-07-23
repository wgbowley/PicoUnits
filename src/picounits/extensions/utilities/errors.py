"""
Filename: parser_errors.py

Description:
    Defines the parser errors classes to 
    ensure descriptive error messages are
    returned to the user
"""

from abc import ABC, abstractmethod
from typing import Any
from pathlib import Path



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


class UnbalancedDepth(Exception):
    """ Exception for unbalanced parentheses or brackets when parsing """
    def __init__(self, caller: str, line: str, symbol: str):
        """ Returns a unbalanced depth error """
        msg = f"'{caller}' attempted to parse {line!r} but depth of {symbol!r} is unbalanced."
        super().__init__(msg)


# Notifications / Warning classes
class ParserNotification(ABC):
    """ Abstract base class for parser notifications messages """
    @abstractmethod
    def __init__(self):
        """ Initializes the class and sets the message variable """
        self.message: str = ""

    def display(self) -> None:
        """ Prints the message """
        print(self.message)

    def __str__(self) -> str:
        """ returns the str(message) """
        return str(self.message)


class BackCompatibilityWarning(ParserNotification):
    """ Warning for missing 'format' key in version """
    def __init__(self, file_path: str):
        """ Returns a compatibility warning """
        filename = Path(file_path).name
        note = f"Tip: {filename} missing 'format' key."
        compatibility = "Add 'version.format: 0.1.0' for compatibility."

        # Sets the message for display
        self.message = f"{note} {compatibility}"


class UnitFrameCompatibilityWarning(ParserNotification):
    """ Warning for missing 'unit_frame' in version """
    def __init__(self, filepath: str):
        filename = Path(filepath).name
        note = f"Tip: {filename} missing 'unit_frame'."
        improvement = "Add 'version.unit_frame: (your_derived_units).ut'."

        # Sets the message for display
        self.message = f"{note} {improvement}"
