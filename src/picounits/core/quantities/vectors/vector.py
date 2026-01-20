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

from picounits.core.quantities.packet import Packet
from picounits.core.quantities.factory import Factory


@dataclass(slots=True)
class VectorPacket(Packet, ABC):
    """
    An Abstract Vector Packet: A prefix, value (Any Vector) and Unit

    NOTE: Representation, prefix scaling, comparison, validation
    are not implemented in this base case.
    """

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
