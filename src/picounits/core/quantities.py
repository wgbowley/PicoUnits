"""
Filename: qualities.py
Author: William Bowley
Version: 0.6

Description:
    Defines the Quantity class which is comprised of
    a magnitude, Unit and prefixScale. This class can
    perform complex arithmetic and display methods
"""

from __future__ import annotations

from typing import Any
from dataclasses import dataclass
from math import log10

from picounits.core.dimensions import Dimension
from picounits.core.scales import PrefixScale
from picounits.core.unit import Unit

from picounits.constants import DIMENSIONLESS

from picounits.core.methods.arithmetic import ArithmeticMixin
from picounits.core.methods.functions import FunctionsMixin
from picounits.core.methods.comparison import ComparisonMixin


@dataclass(slots=True)
class Quantity(ArithmeticMixin, FunctionsMixin, ComparisonMixin):
    """
    A Physical Quantity: A Prefix, magnitude and Unit all together

    Allows for complex arithmetic and display methods via Mixin
    inheritance
    """
    magnitude: int | float
    unit: Unit = Dimension.dimensionless()
    prefix: PrefixScale = PrefixScale.BASE

    def __post_init__(self) -> None:
        """ Validates magnitude, unit, prefix """
        if not isinstance(self.magnitude, (int, float)):
            msg = (
                "Quantity.magnitude must be int or float, "
                f"{type(self.magnitude)}"
            )
            raise TypeError(msg)

        if not isinstance(self.unit, Unit):
            msg = f"Quantity.unit must be of type Unit, not {type(self.unit)}"
            raise TypeError(msg)

        if not isinstance(self.prefix, PrefixScale):
            msg = (
                f"Quantity.prefix must be PrefixScale, not {type(self.prefix)}"
            )
            raise TypeError(msg)

        print(f"self.__class__: {self.__class__}")
        print(f"self.__class__ is Quantity: {self.__class__ is Quantity}")

    @property
    def name(self) -> str:
        """ Returns the name as prefix + magnitude + unit """
        if self.prefix == PrefixScale.BASE:
            return f"{self.magnitude} {self.unit.name}"

        return f"{self.magnitude} {self.prefix.symbol}({self.unit.name})"

    def strip(self) -> int | float:
        """ Scales to base and strips the unit object away """
        base_quantity = self.to_base()
        return base_quantity.magnitude

    def unit_check(self, target: Unit) -> None:
        """ Checks the fundamental units of the Quantity """
        if self.unit != target:
            msg = f"Units are not the same, {self.unit} != {target}"
            raise ValueError(msg)

    def to_scale(self, new_scale: PrefixScale) -> Quantity:
        """ Scales the quantity to target scale """
        if self.prefix == new_scale:
            return self

        prefix_diff = self.prefix.value - new_scale.value
        factor = 10 ** prefix_diff

        return Quantity(self.magnitude * factor, self.unit, new_scale)

    def normalized(self) -> Quantity:
        """ Normalizes the quantity to the closest prefix  """
        magnitude, unit = self.magnitude, self.unit

        # Handles when magnitude equals zero
        if magnitude == 0:
            return Quantity(0, unit, PrefixScale.BASE)

        # Calculates the closet scale and member via log10
        prefix_power = round(log10(abs(magnitude)))
        closest_scale = PrefixScale.from_value(prefix_power)

        # Calculates the new magnitude
        magnitude /= 10 ** closest_scale.value
        return Quantity(magnitude, unit, closest_scale)

    def to_base(self) -> Quantity:
        """ Scales the Quantity to BASE and return """
        if self.prefix == PrefixScale.BASE:
            return self

        # Performs scaling method and returns a new Quantity
        return self.to_scale(PrefixScale.BASE)

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
                        msg = (
                            f"{func.__name__} returned {type(q)}, "
                            "expected Quantity"
                        )
                        raise TypeError(msg)
                    if q.unit != reference:
                        msg = (
                            f"{func.__name__} returned unit {q.unit}, "
                            "expected {reference}"
                        )
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

    def _get_other_quantity(self, other) -> Quantity:
        """ Checking other quantity for arithmetic methods """
        if isinstance(other, Unit):
            raise TypeError("A Quantity magnitude cannot be a Unit")

        if not isinstance(other, Quantity):
            return Quantity(other, DIMENSIONLESS)

        return other.to_base()

    def __repr__(self) -> str:
        """ Displays the Quantity name """
        return self.name
