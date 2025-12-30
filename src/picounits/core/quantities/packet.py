"""
Filename: packet.py
Author: William Bowley
Version: 0.7

Description:
    Defines the abstract base class packet,
    allows usage across implementations avoiding
    circular importation between layers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from picounits.core.unit import Unit
from picounits.constants import DIMENSIONLESS


@dataclass
class QuantityPacket(ABC):
    """
    A physical Quantity Packet: A magnitude and Unit
    """
    magnitude: Any
    unit: Unit

    def unit_check(self, target: QuantityPacket | Unit) -> None:
        """ Uses fundamental dimensions and exponents to check equivalent """
        # Extracts unit from quantity or direct Unit input
        other_unit = target
        if isinstance(target, QuantityPacket):
            other_unit = target.unit

        if self.unit == other_unit:
            return

        msg = f"Units are not the same, {self.unit} != {other_unit}"
        raise ValueError(msg)

    @property
    def is_dimensionless(self) -> bool:
        """ Check if quantity is dimensionless """
        return self.unit == DIMENSIONLESS

    @property
    def stripped(self) -> int | float:
        """ Strips the unit object away, returns non-scaled magnitude """
        return self.magnitude

    @property
    @abstractmethod
    def name(self) -> str:
        """ Returns the Quantities name as magnitude + unit """
        return

    @abstractmethod
    def _get_other_packet(self, other: Any) -> QuantityPacket:
        """ Takes non-Quantity packet, checks and converts if possible """
        return

    def __repr__(self) -> str:
        """ Displays the Quantity name """
        return str(self.name)
