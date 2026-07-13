"""
Filename: construction.py

Description:
    Handles unit and quantity construction 
    via tokenization of the dimensional algebra.
    
    This allows for reconstruction of the Unit,
    which is used to construct the quantity.
"""

from __future__ import annotations

from typing import Any
from picounits.core.scales import PrefixScale
from picounits.core.unit import Unit
from picounits.core.quantities.packet import Packet


class ConstructQuantity:
    """ Constructs a qualities via unit construction """
    @classmethod
    def quantity(cls, value: Any, prefix: str | list, unit: str | list) -> Packet:
        """ Constructs quantity packets from value, prefix and unit strings """
        if isinstance(value, (str, bool)):
            # Handles non-numerical values as non-quantities
            return value

        if isinstance(value, list):
            # Handles simple lists and nested arrays of quantities
            return cls._array(value, prefix, unit)

        # Lookups prefix via symbol
        # prefix = Prefix construction

        # Finds and creates the unit object

        return None # Temp. placeholder

    @classmethod
    def _array(cls, value: Any, prefix: str | list, unit: str | list) -> Packet:
        """ Constructs a series of packets or uses a packet array """
        _, _, _ = value, prefix, unit
        return None # Temp. placeholder

    @classmethod
    def _nested_array(cls, value: Any, prefix: str | list, unit: str | list) -> Packet:
        """ Constructs a nested array into a nested quality array """
        _, _, _ = value, prefix, unit
        return None # Temp. placeholder


class ConstructPrefix:
    """ Constructs a prefix via token analysis """
    @classmethod
    def construct_prefix(cls, prefix: str) -> PrefixScale:
        """ Constructs a prefix via the o(1) prefix lookup """
        _ = prefix
        return None # Temp. placeholder


class ConstructUnits:
    """ Constructs a unit via token analysis """
    @classmethod
    def construct_unit(cls, unit_str: str) -> Unit:
        """ Construct unit from parsed unit strings """
        _ = unit_str
        return None # Temp. placeholder

    @classmethod
    def _tokenize_unit(cls, unit_str: str) -> list[str]:
        """ Returns a tokenized unit string for construction """
        _ = unit_str
        return None # Temp. placeholder

    @classmethod
    def _construct_unit_from_tokens(cls, tokens: list[str]) -> Unit:
        """ Constructs the unit from tokenized unit string """
        _ = tokens
        return None # Temp. placeholder
