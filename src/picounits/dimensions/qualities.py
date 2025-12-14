"""
Filename: Quantities.py
Author: William Bowley
Version: 0.3

Description:
    This file defines the 'Quantity'
    class and its helper function '_combine_unit'
"""

from dataclasses import dataclass
from picounits.dimensions.units import Unit, Dimension, SIBase, conversion


# Definition of a dimensionless unit
_DIMENSIONLESS = Unit(Dimension(base=SIBase.DIMENSIONLESS))


def _combine_unit(first: Unit, second: Unit, division: bool = False) -> Unit:
    """ Combines or divides two units via their dimension exponents """
    combined_dims = {}
    for dim in first.dimensions:
        key = dim.base
        combined_dims[key] = (dim.prefix, dim.exponent)

    for dim in second.dimensions:
        key = dim.base
        # Exponents rules (Power of a product and Quotient of powers)
        exponent_change = dim.exponent * (-1 if division else 1)

        # When theirs a matching base pair, the exponents combine together
        if key in combined_dims:
            prefix, current_exponent = combined_dims[key]
            new_exponent = current_exponent + exponent_change
            combined_dims[key] = (prefix, new_exponent)
        else:
            combined_dims[key] = (dim.prefix, dim.exponent)

    """
    Updates to units might allow for this to be removed.
    """
    # Removes the dimensions that have zero as an exponent
    new_dims = []
    for base, (prefix, exponent) in combined_dims.items():
        if exponent != 0:
            new_dims.append(
                Dimension(prefix=prefix, base=base, exponent=exponent)
            )

    # Handles dimensionless edge case
    if not new_dims:
        return _DIMENSIONLESS

    return Unit(*new_dims)


@dataclass
class Quantity:
    """
    Represents a quantity within the framework with both magnitude and unit
    """
    magnitude: float | int
    unit: Unit

    def to_quantity(self, target_unit: Unit) -> 'Quantity':
        """
        Converts the quantity to a target unit and
        returns a new Quantity object
        """
        new_value, new_unit = conversion(
            self.magnitude, self.unit, target_unit
        )
        return Quantity(new_value, new_unit)

    def _get_other_quantity(self, other):
        """ Checking other quantity method for arithmetic methods """
        if not isinstance(other, Quantity):
            # Handles non-quantity as dimensionless quantities
            return Quantity(other, _DIMENSIONLESS)

        return other

    """ Dunder methods for forward/reverse arithmetic and others """

    def __add__(self, other: 'Quantity') -> 'Quantity':
        """ Defines behavior for forward addition operator """
        other = self._get_other_quantity(other)

        # Other unit scaling and addition of quantities
        converted_other = other.to_quantity(self.unit)
        new_value = self.magnitude + converted_other.magnitude

        return Quantity(new_value, self.unit)

    def __sub__(self, other: 'Quantity') -> 'Quantity':
        """ Defines behavior for forward subtraction operator """
        other = self._get_other_quantity(other)

        # Other unit scaling and subtraction of quantities
        converted_other = other.to_quantity(self.unit)
        new_value = self.magnitude - converted_other.magnitude

        return Quantity(new_value, self.unit)

    def __mul__(self, other: 'Quantity') -> 'Quantity':
        """ Defines behavior for the forward multiplication operator """
        other = self._get_other_quantity(other)

        new_value = self.magnitude * other.magnitude
        new_unit = _combine_unit(self.unit, other.unit)

        return Quantity(new_value, new_unit)

    def __truediv__(self, other: 'Quantity') -> 'Quantity':
        """ Defines behavior for the forward true division operator """
        other = self._get_other_quantity(other)
        if other.magnitude == 0:
            msg = "True division failed: Cannot divide a Quantity by zero"
            raise ZeroDivisionError(msg)

        new_value = self.magnitude / other.magnitude
        new_unit = _combine_unit(self.unit, other.unit, True)

        return Quantity(new_value, new_unit)

    def __floordiv__(self, other: 'Quantity') -> 'Quantity':
        """ Defines behavior for the forward floor division operator """
        other = self._get_other_quantity(other)
        if other.magnitude == 0:
            msg = "Floor division failed: Cannot divide a Quantity by zero"
            raise ZeroDivisionError(msg)

        new_value = self.magnitude // other.magnitude
        new_unit = _combine_unit(self.unit, other.unit, True)

        return Quantity(new_value, new_unit)

    def __mod__(self, other: 'Quantity') -> 'Quantity':
        """ Defines behavior for the forward modulo operator """
        other = self._get_other_quantity(other)
        if other.magnitude == 0:
            msg = "Modulo failed: Cannot modulo a Quantity by zero"
            raise ZeroDivisionError(msg)

        if other.unit != Unit(_DIMENSIONLESS):
            msg = (
                "Modulo failed: "
                "Cannot perform modulo operator when both are Quantity"
            )
            raise TypeError(msg)

        new_value = self.magnitude % other.magnitude
        return Quantity(new_value, self.unit)

    def __pow__(self, other: 'Quantity') -> 'Quantity':
        """ Defines behavior for the forward power operator """
        other = self._get_other_quantity(other)
        if other.unit != Unit(_DIMENSIONLESS):
            msg = (
                "Power failed: "
                "Cannot perform power operator when both are Quantity"
            )
            raise TypeError(msg)

        # Exponent rules: Zero Exponent
        if other.magnitude == 0:
            return Quantity(1.0, Unit(_DIMENSIONLESS))

        new_dims = [
            Dimension(
                prefix=dim.prefix,
                base=dim.base,
                exponent=dim.exponent * other.magnitude
            )
            for dim in self.unit.dimensions
        ]

        # Removes any dimensions that cancel to exponent zero
        new_dims = [dim for dim in new_dims if dim.exponent != 0]

        new_unit = Unit(_DIMENSIONLESS) if not new_dims else Unit(*new_dims)
        new_value = self.magnitude ** other.magnitude

        return Quantity(new_value, new_unit)

    def __radd__(self, other: float | int) -> 'Quantity':
        """ Defines behavior for right-hand addition """
        return self.__add__(other)

    def __rsub__(self, other: float | int) -> 'Quantity':
        """ Defines behavior for right-hand subtraction """

        # Promotes 'other' to a same dimensional quantity
        other_q = Quantity(other, self.unit)
        return other_q.__sub__(self)

    def __rmul__(self, other: float | int) -> 'Quantity':
        """ Defines behavior for right-hand multiplication """
        return self.__mul__(other)

    def __rtruediv__(self, other: float | int) -> 'Quantity':
        """ Defines behavior for right-hand true division """

        # Promote 'other' to a dimensionless Quantity.
        other_q = Quantity(other, Unit(_DIMENSIONLESS))
        return other_q.__truediv__(self)

    def __rfloordiv__(self, other: float | int) -> 'Quantity':
        """ Defines behavior for right-hand floor division """

        # Promote 'other' to a dimensionless Quantity.
        other_q = Quantity(other, Unit(_DIMENSIONLESS))
        return other_q.__floordiv__(self)

    def __rmod__(self, other: float | int) -> 'Quantity':
        """ Defines behavior for right-hand modulo """

        # Promote 'other' to a dimensionless Quantity.
        other_q = Quantity(other, Unit(_DIMENSIONLESS))
        return other_q.__mod__(self)

    def __rpow__(self, other: float | int) -> 'Quantity':
        """ Defines behavior for right-hand power """

        # Promote 'other' to a dimensionless Quantity.
        other_q = Quantity(other, Unit(_DIMENSIONLESS))
        return other_q.__pow__(self)

    def __round__(self, n=0):
        """ Defines behavior for the built-in round() function """
        new_value = round(self.magnitude, n)
        return Quantity(new_value, self.unit)

    def __repr__(self) -> str:
        """ Formatted quantity representation """
        return f"{self.magnitude} {self.unit}"
