"""
Filename: construction.py

Description:
    Handles unit and quantity construction 
    via tokenization of the dimensional algebra.
    
    This allows for reconstruction of the Unit,
    which is used to construct the quantity.
"""

from __future__ import annotations

from typing import Any
from dataclasses import dataclass

from picounits.core.scales import PrefixScale
from picounits.core.dimensions import FBase, Dimension
from picounits.core.unit import Unit
from picounits.core.quantities.packet import Packet
from picounits.core.quantities.factory import Factory

from picounits.extensions.utilities.operations import Operations
from picounits.extensions.utilities.errors import (
    ParserError, UnknownPrefix, ColumnAttribute, UnsupportedType, UnknownOperator
)


@dataclass(slots=True)
class UnitState:
    """ Stores the state of the unit under construction """
    result: Unit = Unit.dimensionless()
    queue_operation: Operations | None = None
    pending_unit: Unit | None = None
    pending_power: int | None = None


class ConstructQuantity:
    """ Constructs a qualities via unit construction """
    @classmethod
    def quantity(cls, value: Any, prefix: str | list, unit: str | list) -> Packet:
        """ Constructs quantity packets from value, prefix and unit strings """
        if isinstance(value, (str, bool)):
            # Handles non-numerical values as non-quantities
            return value

        if isinstance(value, list):
            # Handles simple lists and nested arrays of quantities
            return cls._array(value, prefix, unit)

        # Construct prefix & unit objects
        prefix_obj = ConstructPrefix.construct_prefix(prefix)
        unit_obj = ConstructUnits.construct_unit(unit)

        # Creates the qualities via the quality factory
        return Factory.create(value, unit_obj, prefix_obj)

    @classmethod
    def _array(cls, value: Any, prefix: str | list, unit: str | list) -> Packet:
        """ Constructs a series of packets or uses a packet array """
        if value and isinstance(value[0], list):
            # Nested array check (list of lists)
            if isinstance(unit, list) and len(unit) > 1:
                # Applies different units to each column
                return cls._nested_array(value, prefix, unit)

        # Simple lists, create array quantity e.x [10, 2] (kg*m*s^-2)
        prefix_obj = ConstructPrefix.construct_prefix(prefix)
        unit_obj = ConstructUnits.construct_unit(unit)

        # Creates the qualities via the quality factory
        return Factory.create(value, unit_obj, prefix_obj)

    @classmethod
    def _nested_array(cls, value: Any, prefix: str | list, unit: str | list) -> Packet:
        """ Constructs a nested array into a nested quality array """
        result = []
        for sublist in value:
            row = []
            for index, row_value in enumerate(sublist):
                # Finds the prefix for that column data
                column_prefix = cls._column_prefix(prefix, index)

                # Finds the unit for that column data
                column_unit = cls._column_unit(unit, index)

                # Builds the nested array as a array of quantities
                row.append(cls.quantity(row_value, column_prefix, column_unit))
            result.append(row)
        return result

    @classmethod
    def _column_prefix(cls, prefix: str | list, index: int) -> str:
        """ Finds the prefix for a specific column """
        if isinstance(prefix, list):
            # Applies prefix if available
            if 0 <= index < len(prefix):
                return prefix[index]

            raise ColumnAttribute(prefix)

        # Defaults to base prefix.
        return ""

    @classmethod
    def _column_unit(cls, unit: list, index: int) -> str:
        """ Finds the unit for a specific column """
        if 0 <= index < len(unit):
            return unit[index]

        raise ColumnAttribute(unit)


class ConstructPrefix:
    """ Constructs a prefix via token analysis """
    @classmethod
    def construct_prefix(cls, prefix: str) -> PrefixScale:
        """ Constructs a prefix via the o(1) prefix lookup """
        prefix_scale = PrefixScale.from_symbol(prefix.strip())
        if prefix_scale:
            return prefix_scale

        # Unknown prefix error
        valid_prefixes = PrefixScale.all_symbols()
        raise UnknownPrefix(prefix, valid_prefixes)


class ConstructUnits:
    """ Constructs a unit via token analysis """
    @classmethod
    def construct_unit(cls, unit_str: str) -> Unit:
        """ Construct unit from parsed unit strings """
        if not isinstance(unit_str, str):
            # Handles unknown types by rasing a construction error
            raise UnsupportedType(type(unit_str))

        if not unit_str:
            # Handles dimensionless values
            return Unit.dimensionless()

        # Tokenizes the unit and than constructs the unit object
        tokens = cls._tokenize_unit(unit_str)

        if not tokens:
            # If no tokens returns dimensionless
            return Unit.dimensionless()

        if len(tokens) == 1:
            # Handles case of a single dimensions within the unit
            dimension = FBase.from_symbol(tokens[0])

            if not dimension:
                # Attempts to handle using derived units
                cls._derived_unit(tokens[0])

            return Unit(Dimension(dimension))

        return cls._construct_unit_from_tokens(tokens)

    @classmethod
    def _tokenize_unit(cls, unit_str: str) -> list[str]:
        """ Returns a tokenized unit string for construction """
        for operation in Operations.all_symbols():
            unit_str = unit_str.replace(operation, f" {operation} ")

        # Creates token by splitting at whitespaces
        tokens = unit_str.split()
        return tokens

    @classmethod
    def _derived_unit(cls, token: str) -> Unit | None:
        """ Attempts to handles case of a single dimension within the unit """
        try:
            return None # === placeholder for derived units ===

        except KeyError:
            symbols = FBase.all_symbols()
            msg = f"{token!r} is fan unknown dimension. Supported dimensions are {symbols!r}"
            raise ParserError(cls.__name__, msg) from None

    @classmethod
    def _construct_unit_from_tokens(cls, tokens: list[str]) -> Unit:
        """ Constructs the unit from tokenized unit string """
        # Initializes the unit state dataclass
        state = UnitState()

        for token in tokens:
            symbol = FBase.from_symbol(token)
            if symbol:
                # Constructs pending unit for future operation
                state.pending_unit = Unit(Dimension(symbol))
                continue

            try:
                # Not a base symbol, try operation
                operation = Operations.from_symbol(token)
            except UnknownOperator:
                try:
                    state = cls._updates_pending_powers(token, state)
                    continue

                except ValueError:
                    pass

                msg = f"Unknown token {token!r}"
                raise ParserError(cls.__name__, msg) from None

            if operation is Operations.POWER:
                # Power operation will occur next iteration
                continue

            # Applies pending units before changing operation
            if state.pending_unit is not None:
                match state.queue_operation:
                    case Operations.MULTIPLICATION:
                        state.result *= state.pending_unit
                    case Operations.DIVIDED:
                        state.result /= state.pending_unit
                    case None:
                        state.result = state.pending_unit
                state.pending_unit = None

            # Updates the queued operation
            state.queue_operation = operation

        # Last dimension operations
        if state.pending_unit is not None:
            match state.queue_operation:
                case Operations.MULTIPLICATION:
                    state.result *= state.pending_unit
                case Operations.DIVIDED:
                    state.result /= state.pending_unit
                case None:
                    state.result = state.pending_unit

        return state.result

    @classmethod
    def _updates_pending_powers(cls, token: str, state: UnitState) -> UnitState:
        """ Constructs pending power for next iteration """
        exponent = int(token)
        if state.pending_unit is not None:
            # Updates pending unit, clears pending power and returns state
            state.pending_unit = state.pending_unit ** exponent
            state.pending_power = None

            return state
