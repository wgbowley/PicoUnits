"""
Filename: comparison.py
Author: William Bowley
Version: 0.1

Description:
    Defines the Mixin for comparison dunder methods
    under 'ComparisonMixin'

    NOTE:
    Due to implementation structure methods cannot be typed hinted
    but a general rule is that if it mutates, its a new Quantity
"""

from typing import Any

from picounits.core.unit import Unit


class ComparisonMixin:
    """ Contains the dunder methods for comparison between Quantities """

    @staticmethod
    def error_check(unit1: Unit, unit2: Unit) -> None:
        """ Raises an error if unit1 != unit2 """
        if unit1 != unit2:
            msg = f"Cannot compare different units, {unit1} != {unit2}"
            raise ValueError(msg)

    def __lt__(self, other: Any) -> bool:
        """ Defines the behavior for less than comparison """
        other = self._get_other_quantity(other)

        # Scales magnitude and prefix to BASE
        s_based, o_based = self.to_base(), other.to_base()
        self.error_check(s_based.unit, o_based.unit)

        return s_based.magnitude < o_based.magnitude

    def __le__(self, other) -> bool:
        """  Defines the behavior for Less than or equal comparison"""
        other = self._get_other_quantity(other)

        # Scales magnitude and prefix to BASE
        s_based, o_based = self.to_base(), other.to_base()
        self.error_check(s_based.unit, o_based.unit)

        return s_based.magnitude <= o_based.magnitude

    def __gt__(self, other) -> bool:
        """  Defines the behavior for Greater than comparison"""
        other = self._get_other_quantity(other)

        # Scales magnitude and prefix to BASE
        s_based, o_based = self.to_base(), other.to_base()
        self.error_check(s_based.unit, o_based.unit)

        return s_based.magnitude > o_based.magnitude

    def __ge__(self, other) -> bool:
        """  Defines the behavior for Greater than or equal comparison"""
        other = self._get_other_quantity(other)

        # Scales magnitude and prefix to BASE
        s_based, o_based = self.to_base(), other.to_base()
        self.error_check(s_based.unit, o_based.unit)

        return s_based.magnitude >= o_based.magnitude

    def __eq__(self, other) -> bool:
        """  Defines the behavior for Equality comparison"""
        other = self._get_other_quantity(other)

        # Scales magnitude and prefix to BASE
        s_based, o_based = self.to_base(), other.to_base()
        self.error_check(s_based.unit, o_based.unit)

        return s_based.magnitude == o_based.magnitude

    def __bool__(self) -> bool:
        """ Boolean conversion (usage. if statements) """
        return self.magnitude != 0
