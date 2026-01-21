"""
Filename: parser.py
Author: William Bowley
Version: 0.2

Description:
    High-level parser for .uiv (Unit-Informed Values) files.
    Orchestrates tokenization, conversion, and construction.
"""

from __future__ import annotations

from picounits.extensions.utilities.tokenizer import Tokenizer
from picounits.extensions.utilities.construction import Construct
from picounits.extensions.utilities.converter import Converter
from picounits.extensions.utilities.operations import Operations
from picounits.extensions.parser_errors import ParserError

class Parser:
    """ Parser for .uiv (unit informed values) file format """
    @classmethod