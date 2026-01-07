"""
Filename: real.py
Author: William Bowley
Version: 0.9
Clear: X

Description:
    Defines the Real Packet Class which is
    comprised of a Value, Unit and prefixScale.
"""

from math import log10, ceil, trunc, floor
from typing import Any
from dataclasses import dataclass

from picounits.core.unit import Unit
from picounits.core.scales import PrefixScale

from picounits.core.quantities.packet import Packet
from picounits.core.quantities.scalars.scalar import ScalarPacket

from picounits.lazy_imports import import_factory


# Import transcendental logic functions
from picounits.core.quantities.scalars.methods import transcendental as tlops


@dataclass(slots=True)
class RealPacket(ScalarPacket):
    """
    A Real Packet: A prefix, value (integer or float) and Unit

    NOTE: Prefix is init-only, value is held in absolute form
    """
    def __post_init__(self, prefix: PrefixScale) -> None:
        """ Validates value and unit, then mutates value to BASE """
        if not isinstance(self.value, (int, float)):
            factory = import_factory("RealPacket.__post_init__")

            # Attempts to pass the value to the correct type
            return factory.create(self.value, self.unit, prefix)

        if not isinstance(self.unit, Unit):
            msg = f"Unit must be of type 'Unit', not {type(self.unit)}"
            raise TypeError(msg)

        if not isinstance(prefix, PrefixScale):
            msg = f"Prefix must be of type PrefixScale, not {type(prefix)}"
            raise TypeError(msg)

        # Mutates prefix to PrefixScale.BASE and scales value
        if prefix == PrefixScale.BASE:
            return

        # Ex.  Kilo (3) - BASE (0) = 3 Hence scaling of 10^3
        prefix_difference = prefix.value - PrefixScale.BASE.value
        factor = 10 ** prefix_difference
        self.value *= factor

    @property
    def name(self) -> str:
        """ Returns the packet name as value + prefix(unit) """
        value, prefix = self._normalize()
        return f"{value} {prefix}({self.unit.name})"

    @property
    def magnitude(self) -> int | float:
        """ Returns the mathematical absolute value """
        return abs(self.value)

    @property
    def sign(self) -> int:
        """ Returns the sign of self.value """
        if self.value > 0:
            return 1
        elif self.value < 0:
            return -1
        else:
            return 0

    def _normalize(self) -> tuple[float | int, PrefixScale]:
        """ Normalizes the value for packet name representation """
        value = self.value
        if value == 0:
            # Handles division by zero edge case
            return 0, PrefixScale.BASE

        # Uses log10 to approximate power
        magnitude = abs(value)
        prefix_power = int(log10(magnitude))
        test_value = magnitude / (10 ** prefix_power)

        if test_value <= 1.0:
            prefix_power -= 1

        # O(n) prefix lookup & calculation of new value
        closest = PrefixScale.from_value(prefix_power)
        value /= 10 ** closest.value

        return value, closest

    def __format__(self, format_spec: str) -> str:
        """ Formats the string based on user input through 'format_spec'"""
        value, prefix = self._normalize()
        formatted_value = format(value, format_spec)

        return f"{formatted_value} {prefix}({self.unit.name})"

    def __ceil__(self) -> Packet:
        """ Defines the behavior for ceiling method """
        factory = import_factory("RealPacket.__ceil__")
        return factory.create(ceil(self.value), self.unit)

    def __floor__(self) -> Packet:
        """ Defines the behavior for floor method """
        factory = import_factory("RealPacket.__floor__")
        return factory.create(floor(self.value), self.unit)

    def __trunc__(self) -> Packet:
        """ Defines the behavior for trunc method """
        factory = import_factory("RealPacket.__trunc__")
        return factory.create(trunc(self.value), self.unit)

    def __round__(self, ndigits=None):
        """ Defines the behavior for the round operation """
        factory = import_factory("RealPacket.__round__")
        return factory.create(round(self.value, ndigits), self.unit)

    def __eq__(self, other: Any) -> bool:
        """ Defines the behavior for equality comparison """
        q2 = self._get_other_packet(other)
        if self.unit != q2.unit:
            # Unit equality matters
            return False

        return self.value == q2.value

    @staticmethod
    def _valid_comparison(q1: Packet, q2: Packet) -> None:
        """
        Raises a ValueError if q1.unit != q2.unit, if not returns none
        """
        if q1.unit == q2.unit:
            return

        msg = f"Cannot compare different units, {q1.unit} != {q2.unit}"
        raise ValueError(msg)

    def __lt__(self, other: Any) -> bool:
        """ Defines the behavior for less than comparison """
        q2 = self._get_other_packet(other)
        self._valid_comparison(self, q2)

        return self.value < q2.value

    def __le__(self, other: Any) -> bool:
        """ Defines the behavior for less than or equal to comparison """
        q2 = self._get_other_packet(other)
        self._valid_comparison(self, q2)

        return self.value <= q2.value

    def __gt__(self, other: Any) -> bool:
        """ Defines the behavior for greater than comparison """
        q2 = self._get_other_packet(other)
        self._valid_comparison(self, q2)

        return self.value > q2.value

    def __ge__(self, other: Any) -> bool:
        """ Defines the behavior for greater than or equal to comparison """
        q2 = self._get_other_packet(other)
        self._valid_comparison(self, q2)

        return self.value >= q2.value

    """
    ================ TRANSCENDENTAL METHODS ================
    """

    def to_radians(self) -> Packet:
        """ If dimensionless, converts the Packet to radians """
        return tlops.to_radians_logic(self)

    def to_degrees(self) -> Packet:
        """ If dimensionless, converts the Packet to degrees """
        return tlops.to_degrees_logic(self)

    def sin(self) -> Packet:
        """ If dimensionless, performs the sine operation on self """
        return tlops.sin_logic(self)

    def cos(self) -> Packet:
        """ If dimensionless, performs the cosine operation on self """
        return tlops.cos_logic(self)

    def tan(self) -> Packet:
        """ If dimensionless, performs the tangent operation on self """
        return tlops.tan_logic(self)

    def csc(self) -> Packet:
        """ If dimensionless, performs the cosecant operation on self """
        return tlops.csc_logic(self)

    def sec(self) -> Packet:
        """ If dimensionless, performs the secant operation on self """
        return tlops.sec_logic(self)

    def cot(self) -> Packet:
        """ If dimensionless, performs the cotangent operation on self """
        return tlops.cot_logic(self)

    def asin(self) -> Packet:
        """ If dimensionless, performs the arc sine operation on self """
        return tlops.asin_logic(self)

    def acos(self) -> Packet:
        """ If dimensionless, performs the arc cosine operation on self """
        return tlops.acos_logic(self)

    def atan(self) -> Packet:
        """ If dimensionless, performs the arc tangent operation on self """
        return tlops.atan_logic(self)

    def atan2(self, other: Any) -> Packet:
        """ Defines the atan2 method for packets """
        q2 = self._get_other_packet(other)
        return tlops.atan2_logic(self, q2)

    def acsc(self) -> Packet:
        """ If dimensionless, performs the arc cosecant operation on self """
        return tlops.acsc_logic(self)

    def asec(self) -> Packet:
        """ If dimensionless, performs the arc secant operation on self """
        return tlops.asec_logic(self)

    def acot(self) -> Packet:
        """ If dimensionless, performs the arc cotangent operation on self """
        return tlops.acot_logic(self)

    def sinh(self) -> Packet:
        """
        If dimensionless, performs the hyperbolic sine operation on self
        """
        return tlops.sinh_logic(self)

    def cosh(self) -> Packet:
        """
        If dimensionless, performs the hyperbolic cosine operation on self
        """
        return tlops.cosh_logic(self)

    def tanh(self) -> Packet:
        """
        If dimensionless, performs the hyperbolic tangent operation on self
        """
        return tlops.tanh_logic(self)

    def csch(self) -> Packet:
        """
        If dimensionless, performs the hyperbolic cosecant operation on self
        """
        return tlops.csch_logic(self)

    def sech(self) -> Packet:
        """
        If dimensionless, performs the hyperbolic secant operation on self
        """
        return tlops.sech_logic(self)

    def coth(self) -> Packet:
        """
        If dimensionless, performs the hyperbolic cotangent operation on self
        """
        return tlops.coth_logic(self)

    def asinh(self) -> Packet:
        """
        If dimensionless, performs the inverse hyperbolic sine operation on
        self
        """
        return tlops.asinh_logic(self)

    def acosh(self) -> Packet:
        """
        If dimensionless, performs the inverse hyperbolic cosine operation on
        self
        """
        return tlops.acosh_logic(self)

    def atanh(self) -> Packet:
        """
        If dimensionless, performs the inverse hyperbolic tangent operation on
        self
        """
        return tlops.atanh_logic(self)

    def acsch(self) -> Packet:
        """
        If dimensionless, performs the inverse hyperbolic cosecant operation on
        self
        """
        return tlops.acsch_logic(self)

    def asech(self) -> Packet:
        """
        If dimensionless, performs the inverse hyperbolic secant operation on
        self
        """
        return tlops.asech_logic(self)

    def acoth(self) -> Packet:
        """
        If dimensionless, performs the inverse hyperbolic cotangent operation
        on self
        """
        return tlops.acoth_logic(self)

    def exp(self) -> Packet:
        """ If dimensionless, performs the exponential operation on self """
        return tlops.exp_logic(self)

    def log(self, base: float | int) -> Packet:
        """ If dimensionless, performs the variable logarithm on self """
        return tlops.log_logic(self, base)

    def log2(self) -> Packet:
        """ If dimensionless, performs the base 2 logarithm on self """
        return tlops.log2_logic(self)

    def log10(self) -> Packet:
        """ If dimensionless, performs the base 10 logarithm on self """
        return tlops.log10_logic(self)

    def nlog(self) -> Packet:
        """ If dimensionless, performs the natural logarithm on self """
        return tlops.nlog_logic(self)
