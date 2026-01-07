"""
Filename: scalar.py
Author: William Bowley
Version: 0.1
Clear: X

Description:
    Defines the semi-abstract ScalarPacket Class
    which is defines arithmetic routing for scalars
    but not representation or prefix scaling
"""

from typing import Any
from abc import ABC
from dataclasses import dataclass

from picounits.core.unit import Unit
from picounits.core.quantities.packet import Packet
from picounits.core.quantities.factory import Factory

from picounits.core.quantities.scalars.methods import arithmetic as acops


@dataclass(slots=True)
class ScalarPacket(Packet, ABC):
    """
    An Abstract Scalar Packet: A prefix, value (Any Scalar) and Unit

    NOTE: Representation, prefix scaling, comparison, validation
    are not implemented in this base case.
    """

    def sqrt(self) -> Packet:
        """ Defines the behavior for taking the square root of a scalar """
        q2 = self._get_other_packet(1 / 2)  # Due to fractional exponent law
        return acops.power_logic(self, q2)

    def cbrt(self) -> Packet:
        """ Defines the behavior for taking the cubic root of a scalar """
        q2 = self._get_other_packet(1 / 3)  # Due to fractional exponent law
        return acops.power_logic(self, q2)

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
        Ex. (1+1j) (s) * m = (1+1j) (s) * 1 (m) => (1+1j) (ms)
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
        """
        Defines behavior for the forward true division (/)
        Also defines the syntactic bridge to move units into quantity
        Ex 10 * m => 10 (m) / s = 10 (ms⁻¹)
        """
        if isinstance(other, Unit):
            q2 = Factory.create(1, other)
        else:
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

    def __abs__(self) -> Packet:
        """ Defines the absolute value operator """
        return Factory.create(self.magnitude, self.unit)

    def __neg__(self) -> Packet:
        """ Defines behavior for negation operator (-quantity) """
        return Factory.create(-self.value, self.unit)

    def __pos__(self) -> Packet:
        """ Defines behavior for unary plus operator (+quantity) """
        return Factory.create(+self.value, self.unit)

    def __bool__(self) -> bool:
        """ Defines behavior for boolean conversion (USES MAGNITUDE) """
        return self.magnitude != 0