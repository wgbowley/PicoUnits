"""
Filename: units.py
Author: William Bowley
Version: 0.3

Description:
    This file defines the 'Unit' class
"""

from __future__ import annotations
from typing import Any

from picounits.core.enums import Dimension, SIBase


class Unit:
    """
    Defines a SI metric unit composed of a singular or multiple 'Dimension'.
    """
    def __init__(self, *dimensions: Dimension) -> None:
        if not dimensions:
            msg = "A unit cannot be defined without any dimensions"
            raise RuntimeError(msg)

        for dim in dimensions:
            if not isinstance(dim, Dimension):
                msg = (
                    f"A unit cannot be defined with {type(dim)} "
                    f"has to be {Dimension}"
                )
                raise ValueError(msg)

        self.dimensions: list[Dimension] = list(dimensions)

        # Removes dimensionless if there are other dimensions
        if self.length > 1:
            self.dimensions = [
                dim for dim in self.dimensions
                if dim.base != SIBase.DIMENSIONLESS
            ]

        # Raises error if SIbase is duplicated in the unit definition
        _duplicated_bases = set()
        for dim in self.dimensions:
            if dim.base in _duplicated_bases:
                msg = f"Cannot define a unit with duplicated bases: {dim.base}"
                raise RuntimeError(msg)
            _duplicated_bases.add(dim.base)

        self.dimensions = sorted(
            self.dimensions,
            key=lambda item: item.base.order
        )

    def _analysis(self, other: Unit, division: bool) -> Unit:
        """
        Combines or divides two units via their dimension exponents.
        Keeps the highest prefix when doing division and/or multiplication
        """
        combined_dims = {}
        for dim in self.dimensions:
            key = dim.base
            combined_dims[key] = (dim.prefix, dim.exponent)

        for dim in other.dimensions:
            key = dim.base
            exponent_change = dim.exponent * (-1 if division else 1)

            if key in combined_dims:
                prefix, current_exponent = combined_dims[key]
                # Add exponents
                new_exponent = current_exponent + exponent_change

                # Keeps the highest prefix
                new_prefix = None
                if dim.prefix.value < prefix.value:
                    new_prefix = prefix
                else:
                    new_prefix = dim.prefix

                combined_dims[key] = (new_prefix, new_exponent)
            else:
                combined_dims[key] = (dim.prefix, exponent_change)

        new_dims = []
        for base, (prefix, exponent) in combined_dims.items():
            if exponent != 0:
                new_dims.append(
                    Dimension(prefix=prefix, base=base, exponent=exponent)
                )

        # Handles dimensionless edge case
        if not new_dims:
            return Unit(Dimension(base=SIBase.DIMENSIONLESS))

        return Unit(*new_dims)

    @property
    def length(self) -> int:
        """ Returns the number of dimensions within the unit """
        return len(self.dimensions)

    @property
    def name(self) -> str:
        """ Returns the units name based on its dimensions """
        return " ".join([str(dim.name) for dim in self.dimensions])

    """ Dunder methods for forward/reverse arithmetic and others """

    def __mul__(self, other: Unit) -> Unit:
        """ Defines behavior for the forward multiplication operator """
        return self._analysis(other, False)

    def __truediv__(self, other: Unit) -> Unit:
        """ Defines behavior for forward true division """
        return self._analysis(other, True)

    def __pow__(self, other: Unit) -> Unit:
        """ Defines behavior for forward power """
        if not isinstance(other, (int, float)):
            msg = (
                "Power Failed: Exponent must be int or float, "
                f"not {type(other)}"
            )
            raise TypeError(msg)

        new_dims = [
            Dimension(dim.prefix, dim.base, dim.exponent * other)
            for dim in self.dimensions
        ]

        return Unit(*new_dims)

    def __rmul__(self, other: Any) -> None:
        """ Defines behavior for the right-hand multiplication """
        msg = f"Cannot multiply a {type(other)} by {type(self).__name__}"
        raise TypeError(msg)

    def __rtruediv__(self, other: Any) -> None:
        """ Defines behavior for the right-hand true division """
        msg = f"Cannot true divide a {type(other)} by {type(self).__name__}"
        raise TypeError(msg)

    def __rpow__(self, other: Any) -> None:
        """ Defines behavior for the right-hand power """
        msg = f"Cannot raise a {type(other)} by {type(self).__name__}"
        raise TypeError(msg)

    def __eq__(self, other) -> bool:
        """ Checks equality between units """
        if not isinstance(other, Unit):
            return False
        if self.length != other.length:
            return False

        self_set = {(d.base, d.prefix, d.exponent) for d in self.dimensions}
        other_set = {(d.base, d.prefix, d.exponent) for d in other.dimensions}
        return self_set == other_set

    def __hash__(self) -> int:
        """
        Calculates a hash based on the dimensions independent of internal order
        """
        dim_tuples = {(d.base, d.prefix, d.exponent) for d in self.dimensions}
        return hash(frozenset(dim_tuples))

    def __repr__(self) -> str:
        """ Displays the formatted unit representation """
        return self.name
