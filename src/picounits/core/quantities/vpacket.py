"""
Filename: vpacket.py
Author: William Bowley
Version: 0.7

Description:
    Defines the abstract base class vpacket,
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
class VPacket(ABC):
    """
    A physical Quantity Packet: A Value and Unit
    """
    value: Any
    unit: Unit

    @property
    def is_dimensionless(self) -> bool:
        """ Check if quantity is dimensionless """
        return self.unit == DIMENSIONLESS

    @property
    def stripped(self) -> Any:
        """ Strips the unit object away, returns non-scaled value """
        return self.value

    @property
    @abstractmethod
    def magnitude(self) -> Any:
        """ Returns the absolute physical size of the value """
        return

    @property
    @abstractmethod
    def name(self) -> str:
        """ Returns the Quantities name as value + unit """
        return

    def unit_check(self, target: VPacket | Unit) -> None:
        """ Uses fundamental dimensions and exponents to check equivalent """
        # Extracts unit from quantity or direct Unit input
        other_unit = target
        if isinstance(target, VPacket):
            other_unit = target.unit

        if self.unit == other_unit:
            return

        msg = f"Units are not the same, {self.unit} != {other_unit}"
        raise ValueError(msg)

    @abstractmethod
    def _get_other_packet(self, other: Any) -> VPacket:
        """ Takes non-Quantity packet, checks and converts if possible """
        return

    def __repr__(self) -> str:
        """ Displays the Quantity name """
        return str(self.name)

    def __hash__(self):
        """ Defines behavior for hashing the Quantity """
        return hash((self.value, self.unit))

    def __str__(self) -> str:
        """ Return string representation of the Quantity name """
        return str(self.name)
