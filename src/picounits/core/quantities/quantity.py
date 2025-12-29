"""
Filename: quantity.py
Author: William Bowley
Version: 0.7

Description:
    Defines the Quantity class which is comprised of
    a magnitude, Unit and prefixScale.This class can
    perform complex arithmetic and display methods.
"""


from __future__ import annotations

from math import log10, ceil
from typing import Any
from dataclasses import dataclass, InitVar

from picounits.core.unit import Unit
from picounits.core.scales import PrefixScale
from picounits.constants import DIMENSIONLESS
from picounits.configuration.picounits import DISPLAY_FIGURES

from picounits.core.quantities.packet import QuantityPacket
from .methods import arithmetic as acops
from .methods import comparison as cnops
from .methods import validators as vsops


@dataclass(slots=True)
class Quantity(QuantityPacket):
    """
    A Physical Quantity: A Prefix, Magnitude and Unit

    Allows for complex arithmetic methods between scalars.
    And also has prefix normalization for display methods

    NOTE: Prefix is init-only (InitVar):
    All quantities are normalized to BASE unit internally
    """
    magnitude: int | float
    unit: Unit
    prefix: InitVar[PrefixScale] = PrefixScale.BASE

    def __post_init__(self, prefix: PrefixScale) -> None:
        """
        Validates magnitude and unit, then mutates magnitude to base
        """
        if not isinstance(self.magnitude, (int, float)):
            msg = f"Magnitude must be int or float, not {type(self.magnitude)}"
            raise TypeError(msg)

        if not isinstance(self.unit, Unit):
            msg = f"Unit must be of type Unit, not {type(self.unit)}"
            raise TypeError(msg)

        if not isinstance(prefix, PrefixScale):
            ptype = type(prefix)   # inline length to long
            msg = f"Prefix must be of type PrefixScale, not {ptype}"
            raise TypeError(msg)

        # Mutates prefix to PrefixScale.Base and scales magnitude
        if prefix == PrefixScale.BASE:
            return

        # Ex.  Kilo (3) - BASE (0) = 3 Hence scaling of 10^3
        prefix_difference = prefix.value - PrefixScale.BASE.value
        factor = 10 ** prefix_difference
        self.magnitude *= factor

    @property
    def stripped(self) -> int | float:
        """ Strips the unit object away, returns non-scaled magnitude """
        return self.magnitude

    @property
    def name(self) -> str:
        """ Returns the Quantities name as prefix + magnitude + unit """
        magnitude, prefix = self._normalize()
        return f"{magnitude} {prefix}({self.unit.name})"

    def _normalize(self) -> tuple[float | int, PrefixScale]:
        """ Normalizes the magnitude for Quantity representation """
        magnitude = self.magnitude

        # Handles division by zero edge case
        if self.magnitude == 0:
            return 0, PrefixScale.BASE

        # Uses log10 to approximate power
        prefix_power = int(log10(abs(self.magnitude)))
        test_magnitude = abs(self.magnitude) / (10 ** prefix_power)

        # If scaled quantity is less than 1, decrease scale by 1
        if test_magnitude < 1.0:
            prefix_power -= 1

        # O(n) prefix lookup
        closest_scale = PrefixScale.from_value(prefix_power)

        # Calculates new magnitude and combines to form a string
        magnitude /= 10 ** closest_scale.value

        # Round magnitude to user defined significant figures
        magnitude = round(magnitude, DISPLAY_FIGURES)
        return magnitude, closest_scale

    def _get_other_packet(self, other: Any) -> Quantity:
        """ Takes non-Quantity packet, checks and converts if possible """
        if isinstance(other, Unit):
            msg = "Magnitude cannot be type Unit, must be either float or int"
            raise TypeError(msg)

        # Highly unlikely to occur (reverse dunder methods shouldn't apply)
        if isinstance(other, Quantity):
            return other

        # Returns a dimensionless non-scaled quantity
        return Quantity(other, DIMENSIONLESS)

    """ User Facing methods - (Instance methods, Dunder methods, etc) """

    def unit_check(self, target: Quantity) -> None:
        """ Uses fundamental dimensions and exponents to check equivalent """
        if self.unit == target.unit:
            return

        msg = f"Units are not the same, {self.unit} != {target.unit}"
        raise ValueError(msg)

    @staticmethod
    def unit_validator(forecast: Unit):
        """
        A decorator for function unit output independent of magnitude,
        raises an error if different

        NOTE: Works for list, tuple, integer and float
        """
        return vsops.check_unit_output(forecast)

    def __add__(self, other: Any) -> Quantity:
        """ Defines the behavior for the forwards addition operator (+)"""
        q2 = self._get_other_packet(other)
        return acops.add_logic(self, q2, self.__class__)

    def __radd__(self, other: Any) -> Quantity:
        """ Defines the behavior for the reverse addition operator (+) """
        # Due to the commutative property of addition (a+b = b+a)
        return self.__add__(other)

    def __iadd__(self, other: Any) -> Quantity:
        """ Defines in-place addition operation (+=) """
        # Due to the commutative property of addition (a+b = b+a)
        return self.__add__(other)

    def __sub__(self, other: Any) -> Quantity:
        """ Defines behavior for the forwards subtraction operator (-) """
        q2 = self._get_other_packet(other)
        return acops.sub_logic(self, q2, self.__class__)

    def __rsub__(self, other: Any) -> Quantity:
        """ Defines the behavior for the reverse subtraction method """
        # Due to subtraction being non-commutative
        q1 = self._get_other_packet(other)
        return q1.__sub__(self)

    def __isub__(self, other: Any) -> Quantity:
        """ Defines in-place subtraction operation (-=) """
        return self.__sub__(self)

    def __mul__(self, other: Any) -> Quantity:
        """ Defines behavior for the forward multiplication (*) """
        if isinstance(other, Unit):
            # Creates a syntactic bridge for moving units into quantity
            q2 = Quantity(1, other)
        else:
            q2 = self._get_other_packet(other)

        return acops.multiplication_logic(self, q2, self.__class__)

    def __rmul__(self, other: Any) -> Quantity:
        """ Defines behavior for the reverse multiplication """
        # Due to the commutative property of multiplication (ab = ba)
        return self.__mul__(other)

    def __imul__(self, other: Any) -> Quantity:
        """ Defines in-place multiplication operation (*=) """
        return self.__mul__(other)

    def __truediv__(self, other: Any) -> Quantity:
        """ Defines behavior for the forward true division (/)"""
        q2 = self._get_other_packet(other)
        return acops.true_division_logic(self, q2, self.__class__)

    def __rtruediv__(self, other: float | int) -> Quantity:
        """ Defines behavior for the reverse true division """
        # Due to division being non-commutative
        q1 = self._get_other_packet(other)
        return q1.__truediv__(self)

    def __itruediv__(self, other: Any) -> Quantity:
        """ Defines in-place division (/=) """
        return self.__truediv__(other)

    def __pow__(self, other: Any) -> Quantity:
        """ Defines behavior for the forward power operator (**) """
        q2 = self._get_other_packet(other)
        return acops.power_logic(self, q2, self.__class__)

    def __rpow__(self, other: float | int) -> Quantity:
        """ Defines behavior for the reverse power """
        q1 = self._get_other_packet(other)
        return q1.__pow__(other)

    def __lt__(self, other: Any) -> bool:
        """ Defines the behavior for less than comparison """
        q2 = self._get_other_packet(other)
        return cnops.less_than_comparison_logic(self, q2)

    def __le__(self, other: Any) -> bool:
        """ Defines the behavior for less than or equal to comparison """
        q2 = self._get_other_packet(other)
        return cnops.less_than_or_equal_to_comparison_logic(self, q2)

    def __gt__(self, other: Any) -> bool:
        """ Defines the behavior for greater than comparison """
        q2 = self._get_other_packet(other)
        return cnops.greater_than_comparison_logic(self, q2)

    def __ge__(self, other: Any) -> bool:
        """ Defines the behavior for greater than or equal to comparison """
        q2 = self._get_other_packet(other)
        return cnops.greater_than_or_equal_comparison_logic(self, q2)

    def __eq__(self, other: Any) -> bool:
        """ Defines the behavior for equality comparison """
        q2 = self._get_other_packet(other)
        return cnops.equality_comparison_logic(self, q2)

    def __ceil__(self) -> Quantity:
        """ Defines the behavior for ceiling method """
        return Quantity(ceil(self.magnitude), self.unit)

    def __abs__(self) -> Quantity:
        """ Defines the absolute value operator """
        return Quantity(abs(self.magnitude), self.unit)

    def __neg__(self) -> Quantity:
        """ Defines behavior for negation operator (-quantity) """
        return Quantity(-self.magnitude, self.unit)

    def __pos__(self) -> Quantity:
        """ Defines behavior for unary plus operator (+quantity) """
        return Quantity(+self.magnitude, self.unit)

    def __repr__(self) -> str:
        """ Displays the Quantity normalized name """
        return str(self.name)
