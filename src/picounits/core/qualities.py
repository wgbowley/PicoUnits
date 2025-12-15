"""
Filename: qualities.py
Author: William Bowley
Version: 0.3

Description:
    This file defines the 'Quantity' class
"""

from __future__ import annotations

from typing import Any
from dataclasses import dataclass

from picounits.core.unit import Unit
from picounits.core.conversion import conversion
from picounits.constants import DIMENSIONLESS


@dataclass
class Quantity:
    """
    Represents a quantity within the library with both magnitude and unit
    """
    magnitude: Any
    unit: Unit

    def to_quantity(self, target_unit: Unit) -> Quantity:
        """
        Converts the quantity to a target unit and returns a new quantity
        """
        new_value, new_unit = conversion(
            self.magnitude, self.unit, target_unit
        )
        return Quantity(new_value, new_unit)

    def check_unit_base(self, required_unit: Unit) -> Quantity:
        """ Checks to see if the unit is correct independent of scale """
        self.magnitude, self.unit = (
            conversion(self.magnitude, self.unit, required_unit)
        )

    def _get_other_quantity(self, other):
        """ Checking other quantity method for arithmetic methods """
        if not isinstance(other, Quantity):
            # Handles non-quantity as dimensionless quantities
            return Quantity(other, DIMENSIONLESS)

        return other

    """ Dunder methods for forward/reverse arithmetic  and others """

    def __add__(self, other: Quantity) -> None:
        """ Defines behavior for forward addition operator """
        other = self._get_other_quantity(other)

        # Other unit scaling and addition of quantities
        converted_other = other.to_quantity(self.unit)
        new_value = self.magnitude + converted_other.magnitude

        return Quantity(new_value, self.unit)

    def __sub__(self, other: Quantity) -> Quantity:
        """ Defines behavior for forward subtraction operator """
        other = self._get_other_quantity(other)

        # Other unit scaling and subtraction of quantities
        converted_other = other.to_quantity(self.unit)
        new_value = self.magnitude - converted_other.magnitude

        return Quantity(new_value, self.unit)

    def __mul__(self, other: Quantity) -> Quantity:
        """ Defines behavior for the forward multiplication operator """
        other = self._get_other_quantity(other)

        new_value = self.magnitude * other.magnitude
        new_unit = self.unit * other.unit  

        return Quantity(new_value, new_unit)

    def __truediv__(self, other: Quantity) -> Quantity:
        """ Defines behavior for the forward true division operator """
        other = self._get_other_quantity(other)
        if other.magnitude == 0:
            msg = "True division failed: Cannot divide a Quantity by zero"
            raise ZeroDivisionError(msg)

        new_value = self.magnitude / other.magnitude
        new_unit = self.unit / other.unit

        return Quantity(new_value, new_unit)

    def __floordiv__(self, other: Quantity) -> Quantity:
        """ Defines behavior for the forward floor division operator """
        other = self._get_other_quantity(other)
        if other.magnitude == 0:
            msg = "Floor division failed: Cannot divide a Quantity by zero"
            raise ZeroDivisionError(msg)

        new_value = self.magnitude // other.magnitude
        new_unit = self.unit / other.unit

        return Quantity(new_value, new_unit)

    def __mod__(self, other: Quantity) -> Quantity:
        """ Defines behavior for the forward modulo operator """
        other = self._get_other_quantity(other)
        if other.magnitude == 0:
            msg = "Modulo failed: Cannot modulo a Quantity by zero"
            raise ZeroDivisionError(msg)

        if other.unit != DIMENSIONLESS:
            msg = (
                "Modulo failed: "
                "Cannot perform modulo operator when both are Quantity"
            )
            raise TypeError(msg)

        new_value = self.magnitude % other.magnitude
        return Quantity(new_value, self.unit)

    def __pow__(self, other: Quantity) -> Quantity:
        """ Defines behavior for the forward power operator """
        other = self._get_other_quantity(other)
        if other.unit != DIMENSIONLESS:
            msg = (
                "Power failed: "
                "Cannot perform power operator when both are Quantity"
            )
            raise TypeError(msg)

        # Exponent rules: Zero Exponent
        if other.magnitude == 0:
            return Quantity(1.0, DIMENSIONLESS)

        new_unit = self.unit ** other.magnitude
        new_value = self.magnitude ** other.magnitude

        return Quantity(new_value, new_unit)

    def __radd__(self, other: float | int) -> Quantity:
        """ Defines behavior for right-hand addition """
        return self.__add__(other)

    def __rsub__(self, other: float | int) -> Quantity:
        """ Defines behavior for right-hand subtraction """

        # Promotes 'other' to a same dimensional quantity
        other_q = Quantity(other, self.unit)
        return other_q.__sub__(self)

    def __rmul__(self, other: float | int) -> Quantity:
        """ Defines behavior for right-hand multiplication """
        return self.__mul__(other)

    def __rtruediv__(self, other: float | int) -> Quantity:
        """ Defines behavior for right-hand true division """

        # Promote 'other' to a dimensionless Quantity.
        other_q = Quantity(other, DIMENSIONLESS)
        return other_q.__truediv__(self)

    def __rfloordiv__(self, other: float | int) -> Quantity:
        """ Defines behavior for right-hand floor division """

        # Promote 'other' to a dimensionless Quantity.
        other_q = Quantity(other, DIMENSIONLESS)
        return other_q.__floordiv__(self)

    def __rmod__(self, other: float | int) -> Quantity:
        """ Defines behavior for right-hand modulo """

        # Promote 'other' to a dimensionless Quantity.
        other_q = Quantity(other, DIMENSIONLESS)
        return other_q.__mod__(self)

    def __rpow__(self, other: float | int) -> 'Quantity':
        """ Defines behavior for right-hand power """

        # Promote 'other' to a dimensionless Quantity.
        other_q = Quantity(other, DIMENSIONLESS)
        return other_q.__pow__(self)

    def __round__(self, n=0):
        """ Defines behavior for the built-in round() function """
        new_value = round(self.magnitude, n)
        return Quantity(new_value, self.unit)

    def __repr__(self) -> str:
        """ Formatted quantity representation """
        return f"{self.magnitude} {self.unit}"
