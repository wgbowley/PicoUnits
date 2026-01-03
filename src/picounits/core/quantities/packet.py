"""
Filename: packet.py
Author: William Bowley
Version: 0.8
Clear: X

Description:
    Defines the abstract base class packet,
    acts as standard for the type implementations,
    the functional methods and casing factory.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, InitVar
from typing import Any

from picounits.core.scales import PrefixScale
from picounits.core.unit import Unit


@dataclass
class Packet(ABC):
    """
    A Physical Packet: A Prefix, Value and Unit

    NOTE: Prefix is init-only (InitVar)
    All packets, normalize value to BASE unit during init
    """
    value: Any
    unit: Unit
    prefix: InitVar[PrefixScale] = PrefixScale.BASE

    @abstractmethod
    def __post_init__(self, prefix: PrefixScale) -> None:
        """ Validates value and unit, then mutates value to base """
        return

    def unit_check(self, target: Packet | Unit) -> None:
        """ Uses fundamental dimensions and exponents to check equivalent """
        other_unit = target
        if isinstance(target, Packet):
            other_unit = target.unit

        if self.unit == other_unit:
            return

        msg = f"Units are not the same, {self.unit} != {other_unit}"
        raise ValueError(msg)

    @staticmethod
    def _get_other_packet(other: Any) -> Packet:
        """ Takes non-packet, checks and converts if possible """
        if isinstance(other, Unit):
            msg = "Value cannot be type Unit, must be either float or int"
            raise TypeError(msg)

        if isinstance(other, Packet):
            return other

        if not isinstance(other, (str, bool)):
            # Uses lazy import to avoid circular import between self & factory
            from picounits.core.quantities.factory import Factory
            return Factory.create(other, Unit())

    @abstractmethod
    def _normalize(self) -> tuple[Any, PrefixScale]:
        """
        Normalizes the value for representation and returns value + prefix
        """
        return

    @property
    def stripped(self) -> Any:
        """ Strips the unit object away, returns non-scaled value """
        return self.value

    @property
    @abstractmethod
    def name(self) -> str:
        """ Returns the packet name as value + prefix(unit) """
        return

    @property
    @abstractmethod
    def magnitude(self) -> Any:
        """ Returns the absolute physical size of the value """
        return

    @abstractmethod
    def __format__(self, format_spec: str) -> str:
        """ Formats the string based on user input through 'format_spec' """
        msg = "Subclasses must implement __format__"
        raise NotImplementedError(msg)

    def __repr__(self) -> str:
        """ Displays the packet name """
        return str(self.name)

    def __hash__(self):
        """ Defines behavior for hashing the packet """
        return hash((self.value, self.unit))

    def __str__(self) -> str:
        """ Return string representation of the packet name """
        return str(self.name)
