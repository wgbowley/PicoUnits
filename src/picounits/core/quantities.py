"""
Filename: qualities.py
Author: William Bowley
Version: 0.5

Description:
    This file defines the 'Quantity' class
"""

from __future__ import annotations

from math import log10, radians, degrees, sin, cos, tan, exp, log
from dataclasses import dataclass

from picounits.core.unit import Unit
from picounits.core.scales import PrefixScale
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

    def strip(self) -> int | float:
        """ Scales to base and strips the unit object away """
        base_quantity = self.to_base()
        return base_quantity.magnitude

    def sin(self) -> Quantity:
        """ Performs the sine operation """
        if self.unit is DIMENSIONLESS:
            magnitude = sin(self.magnitude)
            return Quantity(magnitude, self.unit, self.prefix)

        msg ="Trigonometric functions require dimensionless quantities"
        raise ValueError(msg)

    def cos(self) -> Quantity:
        """ Performs the cosine operation """
        if self.unit is DIMENSIONLESS:
            magnitude = cos(self.magnitude)
            return Quantity(magnitude, self.unit, self.prefix)

        msg ="Trigonometric functions require dimensionless quantities"
        raise ValueError(msg)

    def tan(self) -> Quantity:
        """ Performs the tangent operation """
        if self.unit is DIMENSIONLESS:
            magnitude = tan(self.magnitude)
            return Quantity(magnitude, self.unit, self.prefix)

        msg ="Trigonometric functions require dimensionless quantities"
        raise ValueError(msg)

    def exp(self) -> Quantity:
        """ Performs the Exponential operation """
        if self.unit is DIMENSIONLESS:
            magnitude = exp(self.magnitude)
            return Quantity(magnitude, self.unit, self.prefix)

        msg ="Exponential requires dimensionless quantity"
        raise ValueError(msg)

    def log(self) -> Quantity:
        """ Performs the Exponential operation """
        if self.unit is DIMENSIONLESS:
            magnitude = log(self.magnitude)
            return Quantity(magnitude, self.unit, self.prefix)

        msg ="Exponential requires dimensionless quantity"
        raise ValueError(msg)

    def to_radians(self) -> Quantity:
        """ Converts the qunatity to radians """
        if self.unit is DIMENSIONLESS:
            magnitude = radians(self.magnitude)
            return Quantity(magnitude, self.unit, self.prefix)

        raise ValueError("Cannot convert a unit with dimesions to radians")

    def to_degrees(self) -> Quantity:
        """ Converts the qunatity to degrees """
        if self.unit is DIMENSIONLESS:
            magnitude = degrees(self.magnitude)
            return Quantity(magnitude, self.unit, self.prefix)

        raise ValueError("Cannot convert a unit with dimesions to degrees")

    @property
    def name(self) -> str:
        """ Returns the name as prefix + magnitude + unit """
        if self.prefix == PrefixScale.BASE:
            return f"{self.magnitude} {self.unit.name}"

        return f"{self.magnitude} {self.prefix.symbol}({self.unit.name})"

    @staticmethod
    def check(reference: Unit):
        """Returns a decorator that checks the function's unit type"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)

                if reference == DIMENSIONLESS:
                    return result

                def check_quantity(q):
                    if not isinstance(q, Quantity):
                        msg = f"{func.__name__} returned {type(q)}, expected Quantity"
                        raise TypeError(msg)
                    if q.unit != reference:
                        msg = f"{func.__name__} returned unit {q.unit}, expected {reference}"
                        raise TypeError(msg)

                # Single Quantity
                if isinstance(result, Quantity):
                    check_quantity(result)
                    return result

                # Tuple or list of Quantities
                if isinstance(result, (tuple, list)):
                    for item in result:
                        check_quantity(item)
                    return result

                # Anything else is wrong
                msg = (
                    f"{func.__name__} returned {type(result)}, "
                    "expected Quantity or tuple/list of Quantity"
                )
                raise TypeError(msg)

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

        # # Clamp magnitude into [1, 1000) by adjusting prefix power
        # while (abs(magnitude) / 10 ** prefix_power) >= 1000:
        #     prefix_power += 1
        # while (abs(magnitude) / 10 ** prefix_power) < 1:
        #     prefix_power -= 1

        closest_scale = PrefixScale.from_value(prefix_power)

        magnitude /= 10 ** closest_scale.value
        return Quantity(magnitude, unit, closest_scale)

    """ Dunder methods for forward/reverse arithmetic and others """

    def __add__(self, other: Quantity) -> Quantity:
        """ Defines behavior for forward addition """
        other = self._get_other_quantity(other)

        self_b = self.to_base()
        other_b = other.to_base()

        if self_b.unit != other_b.unit:
            msg = f"Cannot add different units, {other_b.unit} != {self_b.unit}"
            raise ValueError(msg)

        new_value = self_b.magnitude + other_b.magnitude
        return Quantity(new_value, self_b.unit).normalized()

    def __radd__(self, other: float | int) -> Quantity:
        return self.__add__(other)

    def __iadd__(self, other: Quantity) -> Quantity:
        """ In-place addition (+=) """
        return self.__add__(other)

    def __sub__(self, other: Quantity) -> Quantity:
        """ Defines behavior for forward subtraction """
        other = self._get_other_quantity(other)

        self_b = self.to_base()
        other_b = other.to_base()

        if self_b.unit != other_b.unit:
            msg = f"Cannot sub different units, {other_b.unit} != {self_b.unit}"
            raise ValueError(msg)

        new_value = self_b.magnitude - other_b.magnitude
        return Quantity(new_value, self_b.unit).normalized()

    def __rsub__(self, other: float | int) -> Quantity:
        return Quantity(other, self.unit).__sub__(self)

    def __isub__(self, other: Quantity) -> Quantity:
        """ In-place subtraction (-=) """
        return self.__sub__(other)

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

    def __imul__(self, other: Quantity) -> Quantity:
        """ In-place multiplication (*=) """
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

    def __itruediv__(self, other: Quantity) -> Quantity:
        """ In-place division (/=) """
        return self.__truediv__(other)

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
            msg = f"Cannot compare different units, {other_b.unit} != {self_b.unit}"
            raise ValueError(msg)

        return self_b.magnitude < other_b.magnitude

    def __le__(self, other: Quantity) -> bool:
        """ Less than or equal comprasion """
        other = self._get_other_quantity(other)

        self_b = self.to_base()
        other_b = other.to_base()

        if self_b.unit != other_b.unit:
            msg = f"Cannot compare different units, {other_b.unit} != {self_b.unit}"
            raise ValueError(msg)

        return self_b.magnitude <= other_b.magnitude

    def __gt__(self, other: Quantity) -> bool:
        """ Greater than comprasion """
        other = self._get_other_quantity(other)

        self_b = self.to_base()
        other_b = other.to_base()

        if self_b.unit != other_b.unit:
            msg = f"Cannot compare different units, {other_b.unit} != {self_b.unit}"
            raise ValueError(msg)

        return self_b.magnitude > other_b.magnitude

    def __ge__(self, other: Quantity) -> bool:
        """ Greather than or equal comprasion """
        other = self._get_other_quantity(other)

        self_b = self.to_base()
        other_b = other.to_base()

        if self_b.unit != other_b.unit:
            msg = f"Cannot compare different units, {other_b.unit} != {self_b.unit}"
            raise ValueError(msg)

        return self_b.magnitude >= other_b.magnitude

    def __eq__(self, other: Quantity) -> bool:
        """ Equality comprasion """
        other = self._get_other_quantity(other)

        self_b = self.to_base()
        other_b = other.to_base()

        if self_b.unit != other_b.unit:
            msg = f"Cannot compare different units, {other_b.unit} != {self_b.unit}"
            raise ValueError(msg)

        return self_b.magnitude == other_b.magnitude

    def __abs__(self) -> Quantity:
        """ Absolute value """
        return Quantity(abs(self.magnitude), self.unit)

    def __neg__(self) -> Quantity:
        """ Negation operator (-quantity) """
        return Quantity(-self.magnitude, self.unit, self.prefix)

    def __pos__(self) -> Quantity:
        """ Unary plus operator (+quantity) """
        return Quantity(+self.magnitude, self.unit, self.prefix)

    def __ceil__(self):
        """ Defines logic for the ceiling method """
        self_b = self.to_base()
        self_b.magnitude = (
            int(self_b.magnitude) + (1 if self_b.magnitude % 1 > 0 else 0)
        )
        return Quantity(self_b.magnitude, self_b.unit).normalized()

    def __bool__(self) -> bool:
        """ Boolean conversion (for if statements) """
        return self.magnitude != 0

    def __round__(self, n=0):
        """ Defines behavior for the built-in round() function """
        return Quantity(round(self.magnitude, n), self.unit, self.prefix)

    def __repr__(self) -> str:
        """ Displays the Quantity name """
        return self.name
    
