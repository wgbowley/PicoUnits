"""
Filename: dsl_parser.py

Description:
    Domain specific language parser for .ut (unit types)
    & .uiv (unit informed values).
    
    Orchestrates deserialization, syntax analysis & 
    construction of units
"""


from pathlib import Path
from typing import IO, Any

from picounits.core.unit import Unit
from picounits.extensions.attribute_loader import DynamicLoader

class Parser:
    """ Parser for .ut & .uiv file formats"""
    @classmethod
    def open(
        cls, filepath: Path | str | IO | Any, derived: Path | str | IO | Any = None
    ) -> DynamicLoader:
        """ Parses .uiv file into an attribute tree structure """
        _, _ = filepath, derived
        return

    @classmethod
    def import_derived(cls, filepath: Path | str | IO | Any) -> dict[str, Unit]:
        """ Parses .ut file and interprets unit strings into runtime registry """
        _ = filepath
        return


class ParseLines:
    """ Parse lines for .ut & .uiv files formats """
    