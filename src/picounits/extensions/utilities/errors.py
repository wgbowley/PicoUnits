"""
Filename: parser_errors.py

Description:
    Defines the parser errors classes to 
    ensure descriptive error messages are
    returned to the user
"""


class UnknownOperator(ValueError):
    """ Exception for unknown operator during construction """
    def __init__(self, char: str, operator: str):
        """ Returns a custom error message """
        msg = f"{char!r} is an unknown operator. Supported operators are {operator!r}"
        super().__init__(msg)


class AmbiguousPower(ValueError):
    """ Exception for ambiguous power syntax """
    def __init__(self, error: str):
        """ Returns a custom error message """
        msg = f"Ambiguous power syntax: {error!r}"
        super().__init__(msg)
