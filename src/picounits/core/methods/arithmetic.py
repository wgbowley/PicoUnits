"""
Filename: arithmetic.py
Author: William Bowley
Version: 0.1

Description:
    Defines the Mixin for arithmetic dunder
    methods and properties under 'MathMixin'

    NOTE:
    Due to implementation structure methods cannot be typed hinted
    but a general rule is that if it mutates, its a new Quantity
"""

from typing import Any

from picounits.core.unit import Unit
from picounits.constants import DIMENSIONLESS


class ArithmeticMixin:
    """ Contains the forward/reverse dunder methods for arithmetic """

    """ Addition Methods """
    def __add__(self, other: Any):
        """ Defines the behavior for the forwards addition operator """
        other = self._get_other_quantity(other)

        # Scales magnitude and prefix to BASE
        s_based, o_based = self.to_base(), other.to_base()

        # Handles non-unit addition
        if s_based.unit != o_based.unit:
            msg = (
                f"Unit mismatch (Addition): {s_based.unit} != {o_based.unit}"
            )
            raise ValueError(msg)

        # Calculates new value, creates the quantity and normalizes it
        new_value = s_based.magnitude + o_based.magnitude
        return self.__class__(new_value, s_based.unit).normalized()

    def __radd__(self, other: Any):
        """ Defines the behavior for the reverse addition method """
        # Due to the commutative property of addition (a+b = b+a)
        return self.__add__(other)

    def __iadd__(self, other: Any):
        """ Defines in-place addition (+=)"""
        return self.__add__(other)

    """ Subtraction Methods """
    def __sub__(self, other: Any):
        """ Defines behavior for the forwards subtraction operator """
        other = self._get_other_quantity(other)

        # Scales magnitude and prefix to BASE
        s_based, o_based = self.to_base(), other.to_base()

        # Handles non-unit subtraction
        if s_based.unit != o_based.unit:
            msg = (
                f"Unit mismatch (subtract): {s_based.unit} != {o_based.unit}"
            )
            raise ValueError(msg)

        # Calculates new value, creates the quantity and normalizes it
        new_value = s_based.magnitude - o_based.magnitude
        return self.__class__(new_value, s_based.unit).normalized()

    def __rsub__(self, other: Any):
        """ Defines the behavior for the reverse subtraction method """
        # Due to subtraction not being commutative unlike addition
        # Has to initiate other as object than subtract self
        other_qty = self._get_other_quantity(other)
        return other_qty.__sub__(self)

    def __isub__(self, other: Any):
        """ Defines in-place subtraction (-=) """
        return self.__sub__(other)

    """ Multiplication methods """
    def __mul__(self, other: Any):
        """ Defines behavior for the forward multiplication """
        if isinstance(other, Unit):
            if self.unit == DIMENSIONLESS:
                return self.__class__(self.magnitude, other, self.prefix)

        other = self._get_other_quantity(other)

        # Scales magnitude and prefix to BASE
        s_based, o_based = self.to_base(), other.to_base()

        # Calculates new_value & new_unit
        new_value = s_based.magnitude * o_based.magnitude
        new_unit = s_based.unit * o_based.unit

        return self.__class__(new_value, new_unit).normalized()

    def __rmul__(self, other: Any):
        """ Defines the behavior for the reverse multiplication """
        # Due to the commutative property of multiplication (ab = ba)
        return self.__mul__(other)

    def __imul__(self, other: Any):
        """ Defines in-place multiplication (*=) """
        return self.__mul__(other)

    """ True Division """
    def __truediv__(self, other: Any):
        """ Defines behavior for the forward true division """
        other = self._get_other_quantity(other)

        # Scales magnitude and prefix to BASE
        s_based, o_based = self.to_base(), other.to_base()

        # Handles the division by zero case
        if o_based.magnitude == 0:
            msg = (
                "True division failed: Cannot divide by zero "
                f"{s_based.magnitude} / {o_based.magnitude}"
            )
            raise ZeroDivisionError(msg)

        # Calculates new_value & new_unit
        new_value = s_based.magnitude / o_based.magnitude
        new_unit = s_based.unit / o_based.unit

        return self.__class__(new_value, new_unit).normalized()

    def __rtruediv__(self, other: float | int):
        """ Defines behavior for the reverse true division """
        if not isinstance(other, (float, int)):
            msg = (
                "Failed: Reverse true division requires (float or int), "
                f"not {type(other)}"
            )
            raise TypeError(msg)

        return (
            self.__class__(other, DIMENSIONLESS).__truediv__(self)
        )

    def __itruediv__(self, other: Any):
        """ Defines in-place division (/=) """
        return self.__truediv__(other)

    """ Power Methods """
    def __pow__(self, other: Any):
        """ Defines behavior for the forward power operator """
        other = self._get_other_quantity(other)

        # Scales magnitude and prefix to BASE
        s_based, o_based = self.to_base(), other.to_base()

        if o_based.unit != DIMENSIONLESS:
            msg = "A unit with dimensions cannot be used as a power"
            raise TypeError(msg)

        if o_based.magnitude == 0:
            return self.__class__(1.0, DIMENSIONLESS)

        # Calculates new_value & new_unit
        new_value = s_based.magnitude ** o_based.magnitude
        new_unit = s_based.unit ** o_based.magnitude

        return self.__class__(new_value, new_unit).normalized()

    def __rpow__(self, other: float | int):
        """ Defines behavior for the reverse power operator """
        return self.__class__(other, DIMENSIONLESS).__pow__(self)

    """ Unary Operators """
    def __abs__(self):
        """ Takes the absolute value of the Quantity.magnitude """
        return self.__class__(abs(self.magnitude), self.unit, self.prefix)

    def __neg__(self):
        """ Takes the negative operator (-Quantity) """
        return self.__class__(-self.magnitude, self.unit, self.prefix)

    def __pos__(self):
        """ Takes the positive operator (+Quantity) """
        return self.__class__(+self.magnitude, self.unit, self.prefix)

    """ Miscellaneous """
    def __ceil__(self):
        """ Defines logic for the celling method """
        s_based = self.to_base()
        s_based.magnitude = (
            int(s_based.magnitude) + (1 if s_based.magnitude % 1 > 0 else 0)
        )
        return self.__class__(s_based.magnitude, s_based.unit).normalized()

    def __round__(self, n=0):
        """ Defines behavior for the built-in round() function """
        return self.__class__(round(self.magnitude, n), self.unit, self.prefix)
