"""
Filename: complex.py
Author: William Bowley
Version: 0.2
Clear: X

Description:
    Defines the Complex Packet Class which is
    comprised of a Value, Unit and prefixScale.
"""

from __future__ import annotations

from math import log10, ceil, degrees, trunc, floor
from cmath import phase
from typing import Any
from dataclasses import dataclass

from picounits.core.unit import Unit
from picounits.core.scales import PrefixScale

from picounits.core.quantities.packet import Packet
from picounits.core.quantities.scalars.scalar import ScalarPacket

from picounits.lazy_imports import import_factory


@dataclass(slots=True)
class ComplexPacket(ScalarPacket):
    """
    A Complex Packet: A prefix, value (Real + Imaginary) and Unit

    NOTE: Prefix is init-only, value is held in absolute form
    """
    def __post_init__(self, prefix: PrefixScale) -> None:
        """ Validates value and unit, then mutates value to Base """
        if not isinstance(self.value, (complex)):
            factory = import_factory("ComplexPacket.__post_init__")

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

        # Ex. Mega (6) - BASE (0) = 6 Hence scaling of 10^6
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
    def real(self) -> Packet:
        """ Returns the real part of self.value """
        factory = import_factory("ComplexPacket.real")
        return factory.create(self.value.real, self.unit)

    @property
    def imag(self) -> Packet:
        """ Returns the imaginary part of self.value """
        factory = import_factory("ComplexPacket.imag")
        return factory.create(self.value.imag, self.unit)

    def conjugate(self) -> ComplexPacket:
        """ Returns the complex conjugate of self.value """
        value: complex = self.value
        return ComplexPacket(value.conjugate(), self.unit)

    def degree_phase(self) -> Packet:
        """ Returns the phase of self.value in degrees """
        phasor = degrees(phase(self.value))

        factory = import_factory("ComplexPacket.degree_phase")
        return factory.create(phasor, Unit.dimensionless())

    def radians_phase(self) -> Packet:
        """ Returns the phase of self.value in radians """
        phasor = phase(self.value)

        factory = import_factory("ComplexPacket.radians_phase")
        return factory.create(phasor, Unit.dimensionless())

    def degrees_polar(self) -> tuple[Packet, Packet]:
        """ Returns the polar representation of the self.value in degrees """
        phasor = degrees(phase(self.value))
        magnitude = self.magnitude

        factory = import_factory("ComplexPacket.degrees_polar")
        return (
            factory.create(phasor, Unit.dimensionless()), 
            factory.create(magnitude, self.unit)
        )

    def radians_polar(self) -> tuple[Packet, Packet]:
        """ Returns the polar representation of the self.value in radians """
        phasor = phase(self.value)
        magnitude = self.magnitude

        factory = import_factory("ComplexPacket.radians_polar")
        return (
            factory.create(phasor, Unit.dimensionless()),
            factory.create(magnitude, self.unit)
        )

    def _normalize(self) -> tuple[complex, PrefixScale]:
        """ Normalizes the value for packet name representation """
        value = self.value
        if value == 0:
            # Handles division by zero edge case
            return 0 + 0j, PrefixScale.BASE

        # Uses log10 to approximate power
        magnitude = abs(value)
        prefix_power = int(log10(magnitude))
        test_value = magnitude / 10 ** prefix_power

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
        real_ceil = ceil(self.value.real)
        imag_ceil = ceil(self.value.imag)

        ceiling = complex(real_ceil, imag_ceil)

        factory = import_factory("ComplexPacket.__ceil__")
        return factory.create(ceiling, self.unit)

    def __floor__(self) -> Packet:
        """ Defines the behavior for floor method """
        new_complex = complex(
            floor(self.value.real),
            floor(self.value.imag)
        )

        factory = import_factory("ComplexPacket.__floor__")
        return factory.create(new_complex, self.unit)


    def __trunc__(self) -> Packet:
        """ Defines the behavior for trunc method """
        new_complex = complex(
            trunc(self.value.real),
            trunc(self.value.imag)
        )

        factory = import_factory("ComplexPacket.__trunc__")
        return factory.create(new_complex, self.unit)


    def __round__(self, ndigits=None):
        """ Defines the behavior for the round operation """
        new_complex = complex(
            round(self.value.real, ndigits),
            round(self.value.imag, ndigits)
        )

        factory = import_factory("ComplexPacket.__round__")
        return factory.create(new_complex, self.unit)

    def __eq__(self, other: Any) -> bool:
        """ Defines the behavior for equality comparison """
        q2 = self._get_other_packet(other)
        if self.unit != q2.unit:
            # Unit equality matters
            return False

        return self.value == q2.value

    def _raise_ordering_error(self) -> None:
        """ Helper for ordering comparison errors """
        msg = (
            "Cannot order complex quantities. "
            "Complex numbers have no natural ordering. "
            "Use abs() to compare magnitudes."
        )
        raise TypeError(msg)

    def __lt__(self, other: Any) -> bool:
        """ Defines the behavior for less than comparison """
        _ = other
        self._raise_ordering_error()

    def __le__(self, other: Any) -> bool:
        """ Defines the behavior for less than or equal to comparison """
        _ = other
        self._raise_ordering_error()

    def __gt__(self, other: Any) -> bool:
        """ Defines the behavior for greater than comparison """
        _ = other
        self._raise_ordering_error()

    def __ge__(self, other: Any) -> bool:
        """ Defines the behavior for greater than or equal to comparison """
        _ = other
        self._raise_ordering_error()


