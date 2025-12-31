"""
Filename: cquantity.py
Author: William Bowley
Version: 0.1

Description:
    Defines the Complex Quantity class which is
    comprised of a Value, Unit and prefixScale.

    This class can perform complex arithmetic and display methods.
"""

from __future__ import annotations

from typing import Any
from math import log10, ceil
from dataclasses import dataclass, InitVar

from picounits.core.unit import Unit
from picounits.core.scales import PrefixScale
from picounits.constants import DIMENSIONLESS
from picounits.configuration.picounits import DISPLAY_FIGURES

from picounits.core.quantities.vpacket import VPacket
from picounits.core.quantities.methods import arithmetic as acops
from picounits.core.quantities.methods import validators as vsops


@dataclass(slots=True)
class CQuantity(VPacket):
    """
    A Complex Physical Quantity: A Prefix, Value and Unit

    Allows for complex arithmetic methods between complex numbers.
    And also has prefix normalization for display methods.

    NOTE: Prefix is init-only (InitVar):
    All quantities are normalized to BASE unit internally
    """
    value: complex
    unit: Unit
    prefix: InitVar[PrefixScale] = PrefixScale.BASE

    def __post_init__(self, prefix: PrefixScale) -> None:
        """
        Validates value and unit, then mutates value to base
        """
        if not isinstance(self.value, (complex)):
            if not isinstance(self.value, (float, int)):
                msg = f"Value must be complex, not {type(self.value)}"
                raise TypeError(msg)

            # Casts floats and integers as complex numbers
            self.value = complex(self.value)

        if not isinstance(self.unit, Unit):
            msg = f"Unit must be of type 'Unit', not {type(self.unit)}"
            raise TypeError(msg)

        if not isinstance(prefix, PrefixScale):
            msg = f"Prefix must be of type PrefixScale, not {type(prefix)}"
            raise TypeError(msg)

        # Mutates prefix to PrefixScale.BASE and scales value
        if prefix == PrefixScale.BASE:
            return

        # Ex. Mega (6) - BASE (0) = 6 Hence scaling of 10^6
        prefix_difference = prefix.value - PrefixScale.BASE.value
        factor = 10 ** prefix_difference
        self.value *= factor

    @property
    def magnitude(self) -> int | float:
        """ Returns the mathematical absolute value (modulus) """
        return abs(self.value)

    @property
    def name(self) -> str:
        """ Returns the Quantities name as prefix + value + unit """
        value, prefix = self._normalize()
        return f"{value} {prefix}({self.unit.name})"

    def _normalize(self) -> tuple[float | int, PrefixScale]:
        """ Normalizes the value for Quantity representation """
        value = self.value
        # Handles division by zero edge case
        if self.value == 0:
            return (0 + 0j), PrefixScale.BASE

        # Calculates the modulus than uses log10 to approximate power
        modulus = abs(self.value)
        prefix_power = int(log10(modulus))

        # If scaled quantity is less than 1, decrease scale by 1
        test_value = abs(self.value) / (10 ** prefix_power)
        if test_value < 1.0:
            prefix_power -= 1

        # O(n) prefix lookup and calculates the new values
        closest_scale = PrefixScale.from_value(prefix_power)
        value /= (10 ** closest_scale.value)

        # Round value to user defined significant figures
        figures = DISPLAY_FIGURES   # Inline length too long
        value = complex(round(value.real, figures), round(value.imag, figures))
        return value, closest_scale

    def _get_other_packet(self, other: Any) -> CQuantity:
        """ Takes non-Quantity packet, checks and converts if possible """
        if isinstance(other, Unit):
            msg = "Value cannot be type Unit, must be a int, float or complex "
            raise TypeError(msg)

        # Highly unlikely to occur (reverse dunder methods shouldn't apply)
        if isinstance(other, CQuantity):
            return other

        # Returns a dimensionless non-scaled quantity
        return CQuantity(other, DIMENSIONLESS)

    """
    ================ USER FACING METHODS ================
    """

    @staticmethod
    def unit_validator(forecast: Unit):
        """
        A decorator for function unit output independent of value,
        raises an error if different

        NOTE: Works for list, tuple, integer and float
        """
        return vsops.check_unit_output(forecast)

    """
    ================ DUNDER METHODS ================
    """

    def __add__(self, other: Any) -> CQuantity:
        """ Defines the behavior for the forwards addition operator (+)"""
        q2 = self._get_other_packet(other)
        return acops.add_logic(self, q2, self.__class__)

    def __radd__(self, other: Any) -> CQuantity:
        """ Defines the behavior for the reverse addition operator (+) """
        # Due to the commutative property of addition (a+b = b+a)
        return self.__add__(other)

    def __iadd__(self, other: Any) -> CQuantity:
        """ Defines in-place addition operation (+=) """
        # Due to the commutative property of addition (a+b = b+a)
        return self.__add__(other)

    def __sub__(self, other: Any) -> CQuantity:
        """ Defines behavior for the forwards subtraction operator (-) """
        q2 = self._get_other_packet(other)
        return acops.sub_logic(self, q2, self.__class__)

    def __rsub__(self, other: Any) -> CQuantity:
        """ Defines the behavior for the reverse subtraction method """
        # Due to subtraction being non-commutative
        q1 = self._get_other_packet(other)
        return q1.__sub__(self)

    def __isub__(self, other: Any) -> CQuantity:
        """ Defines in-place subtraction operation (-=) """
        return self.__sub__(other)

    def __mul__(self, other: Any) -> CQuantity:
        """
        Defines behavior for the forward multiplication (*)
        Also defines the syntactic bridge to move units into quantity:
        Ex. (1+1j)s * LENGTH = (1+1j)s * (1+1j)m = (1+1j)ms (meter * second)
        """
        if isinstance(other, Unit):
            # Use 1.0 to preserve magnitude and phase.
            q2 = CQuantity(1 + 0.0j, other)
        else:
            q2 = self._get_other_packet(other)

        return acops.multiplication_logic(self, q2, self.__class__)

    def __rmul__(self, other: Any) -> CQuantity:
        """ Defines behavior for the reverse multiplication """
        # Due to the commutative property of multiplication (ab = ba)
        return self.__mul__(other)

    def __imul__(self, other: Any) -> CQuantity:
        """ Defines in-place multiplication operation (*=) """
        return self.__mul__(other)

    def __truediv__(self, other: Any) -> CQuantity:
        """ Defines behavior for the forward true division (/)"""
        q2 = self._get_other_packet(other)
        return acops.true_division_logic(self, q2, self.__class__)

    def __rtruediv__(self, other: float | int) -> CQuantity:
        """ Defines behavior for the reverse true division """
        # Due to division being non-commutative
        q1 = self._get_other_packet(other)
        return q1.__truediv__(self)

    def __itruediv__(self, other: Any) -> CQuantity:
        """ Defines in-place division (/=) """
        return self.__truediv__(other)

    def __pow__(self, other: Any) -> CQuantity:
        """ Defines behavior for the forward power operator (**) """
        q2 = self._get_other_packet(other)
        return acops.power_logic(self, q2, self.__class__)

    def __rpow__(self, other: float | int) -> CQuantity:
        """ Defines behavior for the reverse power """
        q2 = self._get_other_packet(other)
        return q2.__pow__(self)

    def __ceil__(self) -> CQuantity:
        """ Defines the behavior for ceiling method """
        new_value = complex(ceil(self.value.real), ceil(self.value.imag))

        return CQuantity(new_value, self.unit)

    def __neg__(self) -> CQuantity:
        """ Flips the sign of both real and imaginary components. """
        return CQuantity(-self.value, self.unit)

    def __pos__(self) -> CQuantity:
        """ Returns the quantity unchanged """
        return CQuantity(+self.value, self.unit)
