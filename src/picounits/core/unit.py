"""
Filename: units.py
Author: William Bowley
Version: 0.6
Clear: Y

Description:
    Defines the Unit class which is comprised
    of a Dimension dataclass. This class performs
    abstract dimensional analysis using Dimensions.
"""

from __future__ import annotations
from typing import Any

from picounits.core.dimensions import Dimension


class Unit:
    """
    A Physical Unit: A series of different Dimension together

    Allows for abstract dimensional analysis and complex unit
    representation for displaying to the user interface
    """
    # Uses __slots__ to decrease memory overhead per object
    __slots__ = ('dimensions', '_hash_cache', '_name_cache')

    def __init__(self, *dimensions: Dimension) -> None:
        """
        Initialize the unit; assume dimensionless if no dimensions are given
        """
        if not dimensions:
            dimensions = [Dimension.dimensionless()]

        # Handles units defined with non-Dimension's
        for dim in dimensions:
            if isinstance(dim, Dimension):
                continue

            msg = f"Dimensions must be 'Dimension' not {type(dim).__name__}"
            raise ValueError(msg)

        self.dimensions = list(dimensions)
        self._hash_cache = None
        self._name_cache = None

        # Performs checks for consistent representation
        self._remove_dimensionless()
        self._duplicated_bases_check()
        self._sort_order()

    def _remove_dimensionless(self) -> None:
        """ If more than one dimension, remove dimensionless """
        if self.length == 1:
            return

        new_dimensions = []
        for dimension in self.dimensions:
            if dimension != Dimension.dimensionless():
                new_dimensions.append(dimension)

        self.dimensions = new_dimensions

    def _duplicated_bases_check(self) -> None:
        """ Checks for duplicated bases during initialization """
        duplicated_bases = set()

        for dim in self.dimensions:
            if dim.base not in duplicated_bases:
                duplicated_bases.add(dim.base)
                continue

            msg = f"Cannot define a unit with duplicated bases: {dim.base}"
            raise ValueError(msg)

    def _sort_order(self) -> None:
        """ Sorts the dimensions to ensure canonical representation """
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

        # Reconstruct dimensions, filtering out zero exponents (dimensionless)
        new_dimensions: list[Dimension] = []
        for base, exponent in combined.items():
            if exponent != 0:
                new_dimensions.append(Dimension(base, exponent))

        # Handles dimensionless unit if all dimensions canceled out
        if not new_dimensions:
            return Unit()

        return Unit(*new_dimensions)

    @property
    def name(self) -> str:
        """ Returns the units name as dimensions and prefixscale"""
        if self._name_cache is None:
            # Avoid constructing multiple's times through using cache
            self._name_cache = "·".join(str(d.name) for d in self.dimensions)

        return self._name_cache

    @property
    def length(self) -> int:
        """
        Number of distinct dimension bases (e.g., kg·m·s⁻² has length 3)
        """
        return len(self.dimensions)

    def __mul__(self, other: Unit) -> Unit:
        """ Defines behavior for the forward multiplication operator """
        if isinstance(other, Unit):
            return self._dimensional_analysis(other, False)

        return self.__rmul__(other)

    def __rmul__(self, other: Any):
        """
        Acts as a syntactic bridge to Quantity to allow for a cleaner API.
        NOTE: Returned quantity, due import injection cannot hint

        Example: 10 * CURRENT => Quantity(10, CURRENT)
        """
        if not isinstance(other, (float, int)):
            msg = f"Cannot use syntactic bridge with {type(other).__name__}"
            raise ValueError(msg)

        try:
            # Provides a custom error message for the import injection
            from picounits.core.quantities.quantity import Quantity
        except ImportError as e:
            msg = (
                "Could not import 'Quantity' for Unit.__rmul__ "
                "This usually means picounits was not installed correctly "
            )
            raise ImportError(msg) from e

        return Quantity(other, self)

    def __truediv__(self, other: Unit) -> Unit:
        """ Defines behavior for forward true division """
        if isinstance(other, Unit):
            return self._dimensional_analysis(other, True)

        msg = f"Cannot true divide a 'Unit' by {type(other).__name__}"
        raise ValueError(msg)

    def __rtruediv__(self, other: Any):
        """
        Acts as a syntactic bridge to Quantity and reciprocal method
        NOTE: Returned quantity | unit, due import injection cannot hint

        Quantity bridge: 10 / CURRENT = Quantity(10, a⁻¹)
        Reciprocal method : 1 / CURRENT => Unit(A⁻¹)
        """
        if not isinstance(other, (int, float)):
            msg = (
                "Cannot use division method or syntactic bridge with "
                f"{type(other).__name__}"
            )
            raise ValueError(msg)

        try:
            # Provides a custom error message for the import injection
            from old.quantities import Quantity
        except ImportError as e:
            msg = (
                "Could not import 'Quantity' for Unit._rtruediv "
                "This usually means picounits was not installed correctly "
            )
            raise ImportError(msg) from e

        new_dims = [
            Dimension(dim.base, dim.exponent * -1) for dim in self.dimensions
        ]

        if other == 1:
            # Returns the reciprocal of the unit
            return Unit(*new_dims)

        # Returns a quantity with value and reciprocal unit
        return Quantity(other, Unit(*new_dims))

    def __pow__(self, other: int | float) -> Unit:
        """ Defines behavior for forward power method """
        if isinstance(other, (float, int)):
            """ NOTE: Develop method for common fractional powers displayed """
            new_dims = [
                Dimension(dim.base, dim.exponent * other)
                for dim in self.dimensions
            ]
            return Unit(*new_dims)

        msg = f"Exponent must be int or float, not {type(other).__name__}"
        raise TypeError(msg)

    def __rpow__(self, other: Any) -> None:
        """ Defines behavior for the right-hand power """
        msg = f"Cannot raise a {type(other)} to the power of a 'Unit'"
        raise TypeError(msg)

    def __eq__(self, other) -> bool:
        """ Checks equality between units of the same length """
        if not isinstance(other, Unit):
            return False
        if self.length != other.length:
            return False

        return hash(self) == hash(other)

    def __hash__(self) -> int:
        """Hash based on dimensions, order-independent"""
        if self._hash_cache is None:
            dim_tuples = {(d.base, d.exponent) for d in self.dimensions}
            self._hash_cache = hash(frozenset(dim_tuples))

        return self._hash_cache

    def __str__(self) -> str:
        """ returns the unit name as a string"""
        return self.name

    def __repr__(self) -> str:
        """ Displays the unit name """
        return f"<Unit: {self.name}>"
