"""
Filename: vectors.py
Author: William Bowley
Version: 0.1
Clear: X

Description:
    Defines the semi-abstract VectorPacket Class
    which is defines arithmetic routing for vector
    but not representation or prefix scaling
"""

from abc import ABC
from typing import Any
from dataclasses import dataclass

from picounits.core.unit import Unit
from picounits.core.quantities.packet import Packet
from picounits.core.quantities.factory import Factory

from picounits.core.quantities.vectors.methods import arithmetic as acops
from picounits.core.quantities.vectors.methods import operations as osops


@dataclass(slots=True)
class VectorPacket(Packet, ABC):
    """
    An Abstract Vector Packet: A prefix, value (Any Vector) and Unit

    NOTE: Representation, prefix scaling, comparison, validation
    are not implemented in this base case.
    """

    @property
    def unit_vector(self) -> Packet:
        """ Calculates the unit vector of self """
        return osops.normalize(self)

    def dot(self, other: Packet) -> Packet:
        """ Defines the behavior for the dot product method """
        return osops.dot(self, other)

    def cross(self, other: Packet) -> Packet:
        """ Defines the behavior for the cross product method"""
        return osops.cross(self, other)

    def angle_between(self, other: Packet) -> Packet:
        """
        Defines the behavior for the angle between method. Returns in radians
        """
        return osops.angle_between(self, other)

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

    def _raise_ordering_error(self) -> None:
        """ Helper for ordering comparison errors """
        msg = (
            "Cannot order vector quantities. "
            "Vectors have no natural ordering. "
            "Use abs() or .magnitude to compare magnitudes."
        )
        raise TypeError(msg)

    def __lt__(self, other: Any) -> bool:
        """ Defines the behavior for less than comparison """
        _ = other
        self._raise_ordering_error()

    def __le__(self, other: Any) -> bool:
        """ Defines the behavior for less than or equal to comparison """
        _ = other
        self._raise_ordering_error()

    def __gt__(self, other: Any) -> bool:
        """ Defines the behavior for greater than comparison """
        _ = other
        self._raise_ordering_error()

    def __ge__(self, other: Any) -> bool:
        """ Defines the behavior for greater than or equal to comparison """
        _ = other
        self._raise_ordering_error()

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
