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


@dataclass
class QuantityPacket(ABC):
    """
    A physical Quantity Packet: A magnitude and Unit
    """
    magnitude: int | float
    unit: Unit

    def unit_check(self, target: QuantityPacket) -> None:
        """ Uses fundamental dimensions and exponents to check equivalent """
        if self.unit == target.unit:
            return

        msg = f"Units are not the same, {self.unit} != {target.unit}"
        raise ValueError(msg)

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
