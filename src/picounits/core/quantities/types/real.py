"""
Filename: real.py
Author: William Bowley
Version: 0.9
Clear: X

Description:
    Defines the Real Packet Class which is
    comprised of a Value, Unit and prefixScale.
"""

from math import log10, ceil
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

    """  ================ TRANSCENDENTAL FUNCTION ================ """

    """ ================ DUNDER METHODS ================ """

    def __format__(self, format_spec: str) -> str:
        """ Formats the string based on user input through 'format_spec'"""
        value, prefix = self._normalize()
        formatted_value = format(value, format_spec)

        return f"{formatted_value} {prefix}({self.unit.name})"

    def __add__(self, other: Any) -> Packet:
        """ Defines the behavior for the forwards addition operator (+) """
        q2 = self._get_other_packet(other)
        return acops.add_logic(self, q2)

    def __radd__(self, other: Any) -> Packet:
        """ Defines the behavior for the reverse addition operator (+) """
        # Due to the commutative property of addition (a+b = b+a)
        return self.__add__(other)

    def __iadd__(self, other: Any) -> Packet:
        """ Defines in-place addition operation (+=) """
        # Due to the commutative property of addition (a+b = b+a)
        return self.__add__(other)

    def __sub__(self, other: Any) -> Packet:
        """ Defines behavior for the forwards subtraction operator (-) """
        q2 = self._get_other_packet(other)
        return acops.sub_logic(self, q2)

    def __rsub__(self, other: Any) -> Packet:
        """ Defines the behavior for the reverse subtraction method """
        # Due to subtraction being non-commutative
        q1 = self._get_other_packet(other)
        return q1.__sub__(self)

    def __isub__(self, other: Any) -> Packet:
        """ Defines in-place subtraction operation (-=) """
        return self.__sub__(other)

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

    def __rmul__(self, other: Any) -> Packet:
        """ Defines behavior for the reverse multiplication """
        # Due to the commutative property of multiplication (ab = ba)
        return self.__mul__(other)

    def __imul__(self, other: Any) -> Packet:
        """ Defines in-place multiplication operation (*=) """
        return self.__mul__(other)

    def __truediv__(self, other: Any) -> Packet:
        """ Defines behavior for the forward true division (/)"""
        q2 = self._get_other_packet(other)
        return acops.true_division_logic(self, q2)

    def __rtruediv__(self, other: float | int) -> Packet:
        """ Defines behavior for the reverse true division """
        # Due to division being non-commutative
        q1 = self._get_other_packet(other)
        return q1.__truediv__(self)

    def __itruediv__(self, other: Any) -> Packet:
        """ Defines in-place division (/=) """
        return self.__truediv__(other)

    def __pow__(self, other: Any) -> Packet:
        """ Defines behavior for the forward power operator (**) """
        q2 = self._get_other_packet(other)
        return acops.power_logic(self, q2)

    def __rpow__(self, other: float | int) -> Packet:
        """ Defines behavior for the reverse power """
        q1 = self._get_other_packet(other)
        return q1.__pow__(self)

    def __ceil__(self) -> Packet:
        """ Defines the behavior for ceiling method """
        return Factory.create(ceil(self.value), self.unit)

    def __abs__(self) -> Packet:
        """ Defines the absolute value operator """
        return Factory.create(self.magnitude, self.unit)

    def __neg__(self) -> Packet:
        """ Defines behavior for negation operator (-quantity) """
        return Factory.create(-self.value, self.unit)

    def __pos__(self) -> Packet:
        """ Defines behavior for unary plus operator (+quantity) """
        return Factory.create(+self.value, self.unit)

    def __eq__(self, other: Any) -> bool:
        """ Defines the behavior for equality comparison """
        q2 = self._get_other_packet(other)
        if self.unit != q2.unit:
            # Unit equality matters
            return False

        return self.value == q2.value

    @staticmethod
    def _valid_comparison(q1: Packet, q2: Packet) -> None:
        """
        Raises a ValueError if q1.unit != q2.unit, if not returns none
        """
        if q1.unit == q2.unit:
            return

        msg = f"Cannot compare different units, {q1.unit} != {q2.unit}"
        raise ValueError(msg)

    def __lt__(self, other: Any) -> bool:
        """ Defines the behavior for less than comparison """
        q2 = self._get_other_packet(other)
        self._valid_comparison(self, q2)

        return self.value < q2.value

    def __le__(self, other: Any) -> bool:
        """ Defines the behavior for less than or equal to comparison """
        q2 = self._get_other_packet(other)
        self._valid_comparison(self, q2)

        return self.value <= q2.value

    def __gt__(self, other: Any) -> bool:
        """ Defines the behavior for greater than comparison """
        q2 = self._get_other_packet(other)
        self._valid_comparison(self, q2)

        return self.value > q2.value

    def __ge__(self, other: Any) -> bool:
        """ Defines the behavior for greater than or equal to comparison """
        q2 = self._get_other_packet(other)
        self._valid_comparison(self, q2)

        return self.value >= q2.value
