"""
Filename: units.py
Author: William Bowley
Version: 0.4
status: N

Description:
    This file defines the 'Unit' class
"""

from __future__ import annotations
from typing import Any

from picounits.core.enums import Dimension, SIBase


class Unit:
    """ Defines a unit composed of one or more Dimensions. """
    def __init__(self, *dimensions: Dimension) -> None:
        """ Initialize the Unit class and performs checks """
        if not dimensions:
            raise ValueError("Cannot define a unit without dimensions")

        for dim in dimensions:
            if not isinstance(dim, Dimension):
                raise ValueError(f"{type(dim).__name__} is not a Dimension")

        self.dimensions = list(dimensions)

        self._remove_dimensionless()
        self._duplicated_bases_check()
        self._sort_order()

    def _remove_dimensionless(self) -> None:
        """Remove dimensionless units when others exist"""
        if self.length == 1:
            return

        new_dims = []
        for dim in self.dimensions:
            if dim.base != SIBase.DIMENSIONLESS:
                new_dims.append(dim)

        self.dimensions = new_dims

    def _duplicated_bases_check(self) -> None:
        """ Checks for duplicated SI bases """
        duplicated_bases = set()

        for dim in self.dimensions:
            if dim.base in duplicated_bases:
                msg = f"Cannot define a unit with duplicated bases: {dim.base}"
                raise ValueError(msg)
            duplicated_bases.add(dim.base)

    def _sort_order(self) -> None:
        """ Sorts the order of dimensions to ensure canonical representation """
        self.dimensions.sort(key=lambda d: d.base.order)


    def _dimensional_analysis(self, other: Unit, division: bool) -> Unit:
        """ Combines or divides two units via their dimension exponents. """
        combined: dict = {dim.base: dim.exponent for dim in self.dimensions}

        for dim in other.dimensions:
            key = dim.base

            # Exponent rules via product and quotient exponent rule
            exponent_change = dim.exponent * (-1 if division else 1)

            if key in combined:
                combined[key] += exponent_change
            else:
                combined[key] = exponent_change

        # Reconstruct dimensions, filtering out zero exponents
        new_dimensions: list[Dimension] = []
        for base, exponent in combined.items():
            if exponent != 0:
                new_dimensions.append(Dimension(base=base, exponent=exponent))

        # Handles dimensionless unit if all dimensions canceled out
        if not new_dimensions:
            return Unit(Dimension(base=SIBase.DIMENSIONLESS))

        return Unit(*new_dimensions)

    @property
    def length(self) -> int:
        """ Returns the number of dimensions within the Unit"""
        return len(self.dimensions)

    @property
    def name(self) -> str:
        """ Returns the units name """
        return " ".join([str(dim.name) for dim in self.dimensions])

    def __mul__(self, other: Unit) -> Unit:
        """ Defines behavior for the forward multiplication operator """
        return self._dimensional_analysis(other, False)

    def __truediv__(self, other: Unit) -> Unit:
        """ Defines behavior for forward true division """
        return self._dimensional_analysis(other, True)

    def __pow__(self, other: int | float) -> Unit:
        """ Defines behavior for forward power """
        if not isinstance(other, (float, int)):
            msg = f"Exponent must be int or float, not {type(other).__name__}"
            raise TypeError(msg)

        new_dims = [
            Dimension(dim.prefix, dim.base, dim.exponent * other)
            for dim in self.dimensions
        ]

        return Unit(*new_dims)

    def __rpow__(self, other: Any) -> None:
        """ Defines behavior for the right-hand power """
        raise TypeError(f"Cannot raise a {type(other)} by a Unit")

    def __eq__(self, other) -> bool:
        """ Checks equality between units """
        if not isinstance(other, Unit):
            return False

        if self.length != other.length:
            return False

        # Compares dimensions independent of their order
        self_set = {(d.base, d.prefix, d.exponent) for d in self.dimensions}
        other_set = {(d.base, d.prefix, d.exponent) for d in other.dimensions}
        return self_set == other_set

    """ Uses local import to avoid circular import across modules """

    def __rmul__(self, other: Any):
        """Defines behavior for the right-hand multiplication"""
        from picounits.core.qualities import Quantity

        return Quantity(other, self)

    def __rtruediv__(self, other: Any):
        """ Defines behavior for the right-hand true division """
        from picounits.core.qualities import Quantity

        if not isinstance(other, (int, float)):
            msg = f"Cannot true divide a {type(other)} by a Unit"
            raise TypeError(msg)

        new_dims = [
            Dimension(dim.prefix, dim.base, dim.exponent * -1)
            for dim in self.dimensions
        ]
        reciprocal_unit = Unit(*new_dims)

        return (
            reciprocal_unit if other == 1 else Quantity(other, reciprocal_unit)
        )

    def __hash__(self) -> int:
        """Hash based on dimensions, order-independent"""
        dim_tuples = {(d.base, d.prefix, d.exponent) for d in self.dimensions}
        return hash(frozenset(dim_tuples))

    def __repr__(self) -> str:
        """ Displays the formatted unit representation """
        return self.name
