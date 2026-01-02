"""
Filename: real.py
Author: William Bowley
Version: 0.9
Clear: X

Description:
    Defines the Real Packet Class which is
    comprised of a Value, Unit and prefixScale.
"""

from math import log10
from typing import Any
from dataclasses import dataclass

from picounits.core.unit import Unit
from picounits.core.scales import PrefixScale

from picounits.core.quantities.packet import Packet
from picounits.core.quantities.factory import Factory

from picounits.core.quantities.methods import arithmetic as acops


@dataclass(slots=True)
class RealPacket(Packet):
    """
    A Real Packet: A prefix, value (integer or float) and Unit

    NOTE: Prefix is init-only, value is held in absolute form
    """
    def __post_init__(self, prefix: PrefixScale) -> None:
        """ Validates value and unit, then mutates value to BASE """
        if not isinstance(self.value, (int, float)):
            # Attempts to pass the value to the correct type
            return Factory.create(self.value, self.unit, prefix)

        if not isinstance(self.unit, Unit):
            msg = f"Unit must be of type 'Unit', not {type(self.unit)}"
            raise TypeError(msg)

        if not isinstance(prefix, PrefixScale):
            msg = f"Prefix must be of type PrefixScale, not {type(prefix)}"
            raise TypeError(msg)

        # Mutates prefix to PrefixScale.BASE and scales value
        if prefix == PrefixScale.BASE:
            return

        # Ex.  Kilo (3) - BASE (0) = 3 Hence scaling of 10^3
        prefix_difference = prefix.value - PrefixScale.BASE.value
        factor = 10 ** prefix_difference
        self.value *= factor

    @property
    def name(self) -> str:
        """ Returns the packet name as value + prefix(unit) """
        value, prefix = self._normalize()
        return f"{value} {prefix}({self.unit.name})"

    @property
    def magnitude(self) -> int | float:
        """ Returns the mathematical absolute value """
        return abs(self.value)

    def _normalize(self) -> tuple[float | int, PrefixScale]:
        """ Normalizes the value for packet name representation """
        value = self.value
        if value == 0:
            # Handles division by zero edge case
            return 0, PrefixScale.BASE

        # Uses log10 to approximate power
        magnitude = abs(value)
        prefix_power = int(log10(magnitude))
        test_value = magnitude / (10 ** prefix_power)

        if test_value < 1.0:
            prefix_power -= 1

        # O(n) prefix lookup & calculation of new value
        closest = PrefixScale.from_value(prefix_power)
        value /= 10 ** closest.value

        return value, closest

    @staticmethod
    def _get_other_packet(other: Any) -> Packet:
        """ Takes non-packet, checks and converts if possible """
        if isinstance(other, Unit):
            msg = "Value cannot be type Unit, must be either float or int"
            raise TypeError(msg)

        if isinstance(other, Packet):
            return other

        if not isinstance(other, (str, bool)):
            return Factory.create(other, Unit())

        msg = f" {Factory.__name__} failed to cast {type(other)} into a packet"
        raise TypeError(msg)

    """ ================ DUNDER METHODS ================ """

    def __add__(self, other: Any) -> Packet:
        """ Defines the behavior for the forwards addition operator (+) """
        q2 = self._get_other_packet(other)
        return acops.add_logic(self, q2)

    def __sub__(self, other: Any) -> Packet:
        """ Defines behavior for the forwards subtraction operator (-) """
        q2 = self._get_other_packet(other)
        return acops.sub_logic(self, q2)

    def __mul__(self, other: Any) -> Packet:
        """
        Defines behavior for the forward multiplication (*)
        Also defines the syntactic bridge to move units into quantity:
        Ex. (1+1j) (s) * LENGTH = (1+1j) (s) * 1 (m) => (1+1j) (ms)
        """
        if isinstance(other, Unit):
            q2 = Factory.create(1, other)
        else:
            q2 = self._get_other_packet(other)

        return acops.multiplication_logic(self, q2)

    def __truediv__(self, other: Any) -> Packet:
        """ Defines behavior for the forward true division (/)"""
        q2 = self._get_other_packet(other)
        return acops.true_division_logic(self, q2)

    def __pow__(self, other: Any) -> Packet:
        """ Defines behavior for the forward power operator (**) """
        q2 = self._get_other_packet(other)
        return acops.power_logic(self, q2)
