"""
Filename: parser_errors.py
Author: William Bowley
Version: 0.1

Description:
    Holds the parser error class to ensure
    no circular imports occur during runtime.
"""


class ParserError(ValueError):
    """ Exception for parser errors when parsing """
    def __init__(self, caller: str, error: str):
        """ Returns a custom error message """
        msg = f"'{caller}' raised error: {error}. "
        super().__init__(msg)
