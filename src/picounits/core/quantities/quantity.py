"""
Filename: quantity.py
Author: William Bowley
Version: 0.7

Description:
    Defines the Quantity class which is comprised of
    a magnitude, Unit and prefixScale.This class can
    perform arithmetic and display methods.
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
from .methods import transcendental as tlops
from .methods import additional as alops


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

    def __format__(self, format_spec: str) -> str:
        """ Formats the string based on user input through 'format_spec' """
        magnitude, prefix = self._normalize()
        formatted_magnitude = format(magnitude, format_spec)

        return f"{formatted_magnitude} {prefix}({self.unit.name})"

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

    """
    ================ USER FACING METHODS ================
    """

    def unit_check(self, target: QuantityPacket | Unit) -> None:
        """ Uses fundamental dimensions and exponents to check equivalent """
        # Extracts unit from quantity or direct Unit input
        other_unit = target
        if isinstance(target, QuantityPacket):
            other_unit = target.unit

        if self.unit == other_unit:
            return

        msg = f"Units are not the same, {self.unit} != {other_unit}"
        raise ValueError(msg)

    @property
    def is_dimensionless(self) -> bool:
        """ Check if quantity is dimensionless """
        return self.unit == DIMENSIONLESS

    @staticmethod
    def unit_validator(forecast: Unit):
        """
        A decorator for function unit output independent of magnitude,
        raises an error if different

        NOTE: Works for list, tuple, integer and float
        """
        return vsops.check_unit_output(forecast)

    def sqrt(self) -> Quantity:
        """ Performs the square root operation on self """
        return acops.square_root_logic(self)

    def cbrt(self) -> Quantity:
        """ Performs the cubic root operation on self """
        return acops.cubic_root_logic(self)

    """
    ================ Transcendental Functions ================
    """

    def to_radians(self) -> Quantity:
        """ If dimensionless, converts the Quantity to radians """
        return tlops.to_radians_logic(self, self.__class__)

    def to_degrees(self) -> Quantity:
        """ If dimensionless, converts the Quantity to degrees """
        return tlops.to_degrees_logic(self, self.__class__)

    def sin(self) -> Quantity:
        """ If dimensionless, performs the sine operation on self """
        return tlops.sin_logic(self, self.__class__)

    def cos(self) -> Quantity:
        """ If dimensionless, performs the cosine operation on self """
        return tlops.cos_logic(self, self.__class__)

    def tan(self) -> Quantity:
        """ If dimensionless, performs the tangent operation on self """
        return tlops.tan_logic(self, self.__class__)

    def csc(self) -> Quantity:
        """ If dimensionless, performs the cosecant operation on self """
        return tlops.csc_logic(self, self.__class__)

    def sec(self) -> Quantity:
        """ If dimensionless, performs the secant operation on self """
        return tlops.sec_logic(self, self.__class__)

    def cot(self) -> Quantity:
        """ If dimensionless, performs the cotangent operation on self """
        return tlops.cot_logic(self, self.__class__)

    def asin(self) -> Quantity:
        """ If dimensionless, performs the arc sine operation on self """
        return tlops.asin_logic(self, self.__class__)

    def acos(self) -> Quantity:
        """ If dimensionless, performs the arc cosine operation on self """
        return tlops.acos_logic(self, self.__class__)

    def atan(self) -> Quantity:
        """ If dimensionless, performs the arc tangent operation on self """
        return tlops.atan_logic(self, self.__class__)

    def atan2(self, other: Any) -> Quantity:
        """ Defines the atan2 method for quantities """
        q2 = self._get_other_packet(other)
        return tlops.atan2_logic(self, q2, self.__class__)

    def acsc(self) -> Quantity:
        """ If dimensionless, performs the arc cosecant operation on self """
        return tlops.acsc_logic(self, self.__class__)

    def asec(self) -> Quantity:
        """ If dimensionless, performs the arc secant operation on self """
        return tlops.asec_logic(self, self.__class__)

    def acot(self) -> Quantity:
        """ If dimensionless, performs the arc cotangent operation on self """
        return tlops.acot_logic(self, self.__class__)

    def sinh(self) -> Quantity:
        """
        If dimensionless, performs the hyperbolic sine operation on self
        """
        return tlops.sinh_logic(self, self.__class__)

    def cosh(self) -> Quantity:
        """
        If dimensionless, performs the hyperbolic cosine operation on self
        """
        return tlops.cosh_logic(self, self.__class__)

    def tanh(self) -> Quantity:
        """
        If dimensionless, performs the hyperbolic tangent operation on self
        """
        return tlops.tanh_logic(self, self.__class__) 

    def csch(self) -> Quantity:
        """
        If dimensionless, performs the hyperbolic cosecant operation on self
        """
        return tlops.csch_logic(self, self.__class__)

    def sech(self) -> Quantity:
        """
        If dimensionless, performs the hyperbolic secant operation on self
        """
        return tlops.sech_logic(self, self.__class__)

    def coth(self) -> Quantity:
        """
        If dimensionless, performs the hyperbolic cotangent operation on self
        """
        return tlops.coth_logic(self, self.__class__)

    def asinh(self) -> Quantity:
        """
        If dimensionless, performs the inverse hyperbolic sine operation on
        self
        """
        return tlops.asinh_logic(self, self.__class__)

    def acosh(self) -> Quantity:
        """
        If dimensionless, performs the inverse hyperbolic cosine operation on
        self
        """
        return tlops.acosh_logic(self, self.__class__)

    def atanh(self) -> Quantity:
        """
        If dimensionless, performs the inverse hyperbolic tangent operation on
        self
        """
        return tlops.atanh_logic(self, self.__class__)

    def acsch(self) -> Quantity:
        """
        If dimensionless, performs the inverse hyperbolic cosecant operation on
        self
        """
        return tlops.acsch_logic(self, self.__class__)

    def acoth(self) -> Quantity:
        """
        If dimensionless, performs the inverse hyperbolic cotangent operation
        on self
        """
        return tlops.acoth_logic(self, self.__class__)

    def exp(self) -> Quantity:
        """ If dimensionless, performs the exponential operation on self """
        return tlops.exp_logic(self, self.__class__)

    def log(self, base: float | int) -> Quantity:
        """ If dimensionless, performs the variable logarithm on self """
        return tlops.log_logic(self, base, self.__class__)

    def log2(self) -> Quantity:
        """ If dimensionless, performs the base 2 logarithm on self """
        return tlops.log2_logic(self, self.__class__)

    def log10(self) -> Quantity:
        """ If dimensionless, performs the base 10 logarithm on self """
        return tlops.log10_logic(self, self.__class__)

    def nlog(self) -> Quantity:
        """ If dimensionless, performs the natural logarithm on self """
        return tlops.nlog_logic(self, self.__class__)

    """
    ================ DUNDER METHODS ================
    """

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
        return self.__sub__(other)

    def __mul__(self, other: Any) -> Quantity:
        """
        Defines behavior for the forward multiplication (*)
        Also defines the syntactic bridge to move units into quantity:
        Ex. 10s * LENGTH = 10s * 1m => 10ms (meter * second)
        """
        if isinstance(other, Unit):
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

    def __hash__(self) -> int:
        """ Defines behavior for hashing the Quantity """
        return alops.hashing_logic(self)

    def __repr__(self) -> str:
        """ Displays the Quantity normalized name """
        return str(self.name)

    def __str__(self) -> str:
        """ Return string representation of Quantity """
        return str(self.name)