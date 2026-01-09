"""
Filename: array.py
Author: William Bowley
Version: 0.1
Clear: X

Description:
    Defines the Array Packet Class which is
    comprised of a Value, Unit and prefixScale.
"""


from __future__ import annotations

from math import log10
from typing import Any
from dataclasses import dataclass

from picounits.core.unit import Unit
from picounits.core.scales import PrefixScale

from picounits.core.quantities.packet import Packet
from picounits.core.quantities.vectors.vector import VectorPacket

from picounits.lazy_imports import import_factory


@dataclass(slots=True)
class ArrayPacket(VectorPacket):
    """
    A Array Packet: A prefix, array and a unit

    NOTE: Prefix is init-only, value is held in absolute form
    """
    def __post_init__(self, prefix: PrefixScale) -> None:
        """ Validates value and unit, then mutates values to BASE """
        if not isinstance(self.value, (list, tuple)):
            factory = import_factory("RealPacket.__post_init__")

            # Attempts to pass the value to the correct type
            return factory.create(self.value, self.unit, prefix)

        if not isinstance(self.unit, Unit):
            msg = f"Unit must be of type 'Unit', not {type(self.unit)}"
            raise TypeError(msg)

        if not isinstance(prefix, PrefixScale):
            msg = f"Prefix must be of type PrefixScale, not {type(prefix)}"
            raise TypeError(msg)

        # Converts the input to a check converted list
        self._quantity_conversion()

        # Mutates prefix to PrefixScale.BASE and scales value
        if prefix == PrefixScale.BASE:
            return


    def _quantity_conversion(self) -> None:
        """Strip packet wrapper and store raw numeric values."""
        new_value: list = []
        for item in self.value:
            if isinstance(item, Packet):
                if self.unit == item.unit:
                    new_value.append(item.value)

            elif isinstance(item, (int, float)):
                new_value.append(item)
            else:
                raise TypeError(f"Cannot convert {type(item)} to ArrayPacket value")

        self.value = new_value
