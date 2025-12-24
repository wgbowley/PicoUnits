"""
Filename: qualities.py
Author: William Bowley
Version: 0.5

Description:
    This file defines the 'Quantity' class
"""

from __future__ import annotations

from math import log10
from dataclasses import dataclass

from picounits.core.unit import Unit
from picounits.core.enums import PrefixScale
from picounits.constants import DIMENSIONLESS


@dataclass(slots=True)
class Quantity:
    """
    Represents a quantity within the library with both magnitude and unit
    """
    magnitude: int | float
    unit: Unit = DIMENSIONLESS
    prefix: PrefixScale = PrefixScale.BASE

    def __post_init__(self) -> None:
        """ Validates magnitude, unit, prefix """
        if not isinstance(self.magnitude, (int, float)):
            raise TypeError(
                f"Quantity magnitude must be int or float, not {type(self.magnitude)}"
            )

        if not isinstance(self.unit, Unit):
            raise TypeError(
                f"Quantity unit must be of type Unit, not {type(self.unit)}"
            )

        if not isinstance(self.prefix, PrefixScale):
            raise TypeError(
                f"Quantity prefix must be PrefixScale, not {type(self.prefix)}"
            )

    @property
    def name(self) -> str:
        """ Returns the name as prefix + magnitude + unit """
        if self.prefix == PrefixScale.BASE:
            return f"{self.magnitude} {self.unit.name}"

        return f"{self.magnitude} {self.prefix.symbol}({self.unit.name})"

    @staticmethod
    def check(reference: Unit):
        """ Returns a decorator that checks the function's unit type """
        def decorator(func):
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)

                if reference == DIMENSIONLESS:
                    return result

                if not isinstance(result, Quantity):
                    msg = f"{func.__name__} returned {type(result)}, expected Quantity"
                    raise TypeError(msg)

                if result.unit != reference:
                    msg = f"{func.__name__} returned unit {result.unit}, expected {reference}"
                    raise TypeError(msg)

                return result
            return wrapper
        return decorator

    def to_scale(self, new_scale: PrefixScale) -> Quantity:
        """ Scales the quantity to target scale """
        if self.prefix == new_scale:
            return self

        prefix_diff = self.prefix.value - new_scale.value
        factor = 10 ** prefix_diff
        return Quantity(self.magnitude * factor, self.unit, new_scale)

    def to_base(self) -> Quantity:
        """ Returns this Quantity scaled to BASE """
        if self.prefix == PrefixScale.BASE:
            return self
        return self.to_scale(PrefixScale.BASE)

    def check_unit(self, reference: Unit) -> None:
        """ Checks the fundamental units of the Quantity """
        if self.unit != reference:
            raise ValueError(
                f"Units are not the same, {self.unit} != {reference}"
            )

    def _get_other_quantity(self, other) -> Quantity:
        """ Checking other quantity for arithmetic methods """
        if isinstance(other, Unit):
            raise TypeError("A Quantity magnitude cannot be a Unit")

        if not isinstance(other, Quantity):
            return Quantity(other, DIMENSIONLESS)

        return other.to_base()

    def normalized(self) -> Quantity:
        """ Normalizes the quantity to the closest prefix and returns a new Quantity """
        magnitude = self.magnitude
        unit = self.unit

        if magnitude == 0:
            return Quantity(0, unit, PrefixScale.BASE)

        prefix_power = round(log10(abs(magnitude)))
        closest_value, member = PrefixScale.from_value(prefix_power)

        magnitude /= 10 ** closest_value
        return Quantity(magnitude, unit, member)

    """ Dunder methods for forward/reverse arithmetic and others """

    def __add__(self, other: Quantity) -> Quantity:
        """ Defines behavior for forward addition """
        other = self._get_other_quantity(other)

        self_b = self.to_base()
        other_b = other.to_base()

        if self_b.unit != other_b.unit:
            raise ValueError(
                f"Cannot add different units, {other_b.unit} != {self_b.unit}"
            )

        new_value = self_b.magnitude + other_b.magnitude
        return Quantity(new_value, self_b.unit).normalized()

    def __radd__(self, other: float | int) -> Quantity:
        return self.__add__(other)

    def __sub__(self, other: Quantity) -> Quantity:
        """ Defines behavior for forward subtraction """
        other = self._get_other_quantity(other)

        self_b = self.to_base()
        other_b = other.to_base()

        if self_b.unit != other_b.unit:
            raise ValueError(
                f"Cannot sub different units, {other_b.unit} != {self_b.unit}"
            )

        new_value = self_b.magnitude - other_b.magnitude
        return Quantity(new_value, self_b.unit).normalized()

    def __rsub__(self, other: float | int) -> Quantity:
        return Quantity(other, self.unit).__sub__(self)

    def __mul__(self, other: Quantity) -> Quantity:
        """ Defines behavior for the forward multiplication """

        # If the quantity is dimensionless, Returns with the unit
        if isinstance(other, Unit):
            if self.unit == DIMENSIONLESS:
                return Quantity(self.magnitude, other, self.prefix)

        other = self._get_other_quantity(other)

        self_b = self.to_base()
        other_b = other.to_base()

        new_value = self_b.magnitude * other_b.magnitude
        new_unit = self_b.unit * other_b.unit
        return Quantity(new_value, new_unit).normalized()

    def __rmul__(self, other: float | int) -> Quantity:
        return self.__mul__(other)

    def __truediv__(self, other: Quantity) -> Quantity:
        """ Defines behavior for the forward true division """
        other = self._get_other_quantity(other)

        self_b = self.to_base()
        other_b = other.to_base()

        if other_b.magnitude == 0:
            raise ZeroDivisionError("True division failed: Cannot divide by zero")

        new_value = self_b.magnitude / other_b.magnitude
        new_unit = self_b.unit / other_b.unit
        return Quantity(new_value, new_unit).normalized()

    def __rtruediv__(self, other: float | int) -> Quantity:
        return Quantity(other, DIMENSIONLESS).__truediv__(self)

    def __pow__(self, other: Quantity) -> Quantity:
        """ Defines behavior for the forward power operator """
        other = self._get_other_quantity(other)

        self_b = self.to_base()
        other_b = other.to_base()

        if other_b.magnitude == 0:
            return Quantity(1.0, DIMENSIONLESS)

        new_value = self_b.magnitude ** other_b.magnitude
        new_unit = self_b.unit ** other_b.magnitude
        return Quantity(new_value, new_unit).normalized()

    def __rpow__(self, other: float | int) -> Quantity:
        return Quantity(other, DIMENSIONLESS).__pow__(self)

    def __lt__(self, other: Quantity) -> bool:
        """ Less than comparsion """
        other = self._get_other_quantity(other)

        self_b = self.to_base()
        other_b = other.to_base()

        if self_b.unit != other_b.unit:
            raise ValueError(
                f"Cannot compare different units, {other_b.unit} != {self_b.unit}"
            )

        return self_b.magnitude < other_b.magnitude

    def __le__(self, other: Quantity) -> bool:
        """ Less than or equal comprasion """
        other = self._get_other_quantity(other)

        self_b = self.to_base()
        other_b = other.to_base()

        if self_b.unit != other_b.unit:
            raise ValueError(
                f"Cannot compare different units, {other_b.unit} != {self_b.unit}"
            )

        return self_b.magnitude <= other_b.magnitude

    def __gt__(self, other: Quantity) -> bool:
        """ Greater than comprasion """
        other = self._get_other_quantity(other)

        self_b = self.to_base()
        other_b = other.to_base()

        if self_b.unit != other_b.unit:
            raise ValueError(
                f"Cannot compare different units, {other_b.unit} != {self_b.unit}"
            )

        return self_b.magnitude > other_b.magnitude

    def __ge__(self, other: Quantity) -> bool:
        """ Greather than or equal comprasion """
        other = self._get_other_quantity(other)

        self_b = self.to_base()
        other_b = other.to_base()

        if self_b.unit != other_b.unit:
            raise ValueError(
                f"Cannot compare different units, {other_b.unit} != {self_b.unit}"
            )

        return self_b.magnitude >= other_b.magnitude

    def __eq__(self, other: Quantity) -> bool:
        """ Equality comprasion """
        other = self._get_other_quantity(other)

        self_b = self.to_base()
        other_b = other.to_base()

        if self_b.unit != other_b.unit:
            raise ValueError(
                f"Cannot compare different units, {other_b.unit} != {self_b.unit}"
            )

        return self_b.magnitude == other_b.magnitude

    def __round__(self, n=0):
        """ Defines behavior for the built-in round() function """
        return Quantity(round(self.magnitude, n), self.unit, self.prefix)

    def __repr__(self) -> str:
        """ Displays the Quantity name """
        return self.name
