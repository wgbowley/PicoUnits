"""
Filename: parser.py
Author: William Bowley
Version: 0.1

Description:
    Defines the Parser for .uiv (Unit-Informed Values) files
"""

from pathlib import Path


class Parser:
    """ Parser for .uiv (Unit-Informed Values) files """
    @classmethod
    def open(cls, file: Path) -> str:
        """ import values and their units """
        with open(file, 'r') as f:
            content = f.read()
            print(content)

Parser.open("examples\parameters.uiv")