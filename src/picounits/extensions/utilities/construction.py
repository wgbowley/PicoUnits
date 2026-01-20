"""
Filename: construction.py
Author: William Bowley
Version: 0.1

Description:
    Handles unit and quantity construction 
    via tokenization of the dimensional algebra.
    This allows for reconstruction of the Unit,
    which is used to construct the quantity.
"""

from typing import Any

from picounits.core.unit import Unit
from picounits.core.scales import PrefixScale
from picounits.core.dimensions import FBase, Dimension
from picounits.core.quantities.packet import Packet
from picounits.core.quantities.factory import Factory

from picounits.extensions.parser_errors import ParserError
from picounits.extensions.utilities.operations import Operations

class Construct:
    """ Stateless construction utility for unit and quantity construction """

    @classmethod
    def _construct_from_tokenized_unit(cls, tokens: list[str]) -> Unit:
        """ Constructs the unit from the tokenized unit string """
        result = Dimension.dimensionless()
        queue_operation = None
        pending_unit = None
        pending_power = None

        # Ensure usage unicode isn't mixed with ^ Ex. m^⁶ only either m^6 or m⁶
        Operations.validate_unicode_usage(tokens)

        for token in tokens:
            symbol = FBase.from_symbol(token)

            if not symbol:
                try:
                    operation = Operations.from_symbol(token)
                except ParserError:
                    # Not an operation, try as power
                    try:
                        pending_power = int(token)
                        if pending_unit is not None:
                            pending_unit = pending_unit ** pending_power
                            pending_power = None
                        continue

                    except ValueError as exc:
                        msg = f"'{token}' is unknown in unit expression"
                        raise ParserError(cls.__name__, msg) from exc

                if operation == Operations.POWER:
                    # Handles the power operation for unicode
                    pending_power = Operations.check_unicode_power(operation)
                    if pending_unit is not None:
                        pending_unit **= pending_power
                        pending_power = None

                    continue

                # Matches queue operation and performs that operation
                if pending_unit is not None:
                    if queue_operation == Operations.MULTIPLICATION:
                        result *= pending_unit
                    elif queue_operation == Operations.DIVIDED:
                        result /= pending_unit
                    elif queue_operation is None:
                        result = pending_unit
                    pending_unit = None

                # Loads the new operation into queue
                queue_operation = operation
                continue

            pending_unit = Unit(Dimension(symbol))

        # Finishes any pending power or operations post-loop
        if pending_unit is not None:
            if pending_power is not None:
                pending_unit **= pending_power

            if queue_operation == Operations.MULTIPLICATION:
                result *= pending_unit
            elif queue_operation == Operations.DIVIDED:
                result /= pending_unit
            elif queue_operation is None:
                result = pending_unit

        return result

    @classmethod
    def _tokenize_unit(cls, unit_str: str) -> Unit:
        """ Constructs unit from parsed unit strings """
        if not unit_str:
            # Handles dimensionless values
            return Unit.dimensionless()

        # Splits the unit string into tokenized between operators
        for op in Operations.all_symbols():
            unit_str = unit_str.replace(op, f" {op} ")

        tokens = unit_str.split()

        if len(tokens) == 1:
            # Handles case of a single dimension within the unit
            dim = FBase.from_symbol(tokens[0])
            if not dim:
                symbols = FBase.all_symbols()
                msg = (
                    f"'{tokens[0]}' is an unknown dimension. "
                    f"Supported dimensions are {symbols}"
                )
                raise ParserError(cls.__name__, msg)

            return Unit(Dimension(dim))

        return cls._construct_from_tokenized_unit(tokens)

    @classmethod
    def _construct_prefix(cls, prefix: str) -> PrefixScale:
        """ Constructs a prefix via the o(1) prefix lookup """
        prefix_str = prefix if isinstance(prefix, str) else ""
        prefix_scale = PrefixScale.from_symbol(prefix_str)

        if not prefix_scale:
            if prefix_str:
                prefixes = PrefixScale.all_symbols()
                msg = (
                    f"'{prefix_str}' is an unknown prefix. "
                    f"Supported prefixes are {prefixes}"
                )
                raise ParserError(cls.__name__, msg)

            prefix_scale = PrefixScale.BASE

        return prefix_scale

    @classmethod
    def _nested_arrays(
        cls, value: Any, prefix: str | list, unit: str | list
    ) -> Packet:
        """ Constructs a nested array into a nested quality array"""
        result = []
        for sublist in value:
            row = []
            for index, value in enumerate(sublist):
                # Finds the unit for that columns data
                if index < len(unit):
                    column_unit = unit[index]
                else:
                    column_unit = unit[-1]

                # Finds the prefix for that columns data
                if isinstance(prefix, list):
                    if index < len(prefix):
                        column_prefix = prefix[index]
                    else:
                        column_prefix = prefix[-1]
                elif isinstance(prefix, str):
                    column_prefix = prefix
                else:
                    column_prefix = ""

                # Builds the nested array as a array of quantities
                row.append(cls.quantity(value, column_prefix, column_unit))
            result.append(row)
        return result

    @classmethod
    def _quantity_arrays(
        cls, value: Any, prefix: str | list, unit: str | list
    ) -> Packet:
        """ Constructs a series of packets or uses a packet array """
        # Nested array check (list of lists)
        if value and isinstance(value[0], list):
            # For nested arrays with multiple units
            if isinstance(unit, list) and len(unit) > 1:
                # Apply different unit to each column
                return cls._nested_arrays(value, prefix, unit,)

        # Simple lists, create array quantity e.x [10, 2] (kg*m*s^-2)
        prefix = Construct._construct_prefix(prefix)

        unit_str = unit[0] if isinstance(unit, list) else unit
        unit_obj = cls._tokenize_unit(unit_str)

        return Factory.create(value, unit_obj, prefix)

    @classmethod
    def quantity(
        cls, value: Any, prefix: str | list, unit: str | list
    ) -> Packet:
        """ Constructs a quantity object from prefix, value, unit """
        if isinstance(value, (str, bool)):
            # Handles non-numerical values as non-quantities
            return value

        if isinstance(value, list):
            # Handles simple lists and nested arrays of quantities
            return cls._quantity_arrays(value, prefix, unit)

        # Lookups prefix via symbol
        prefix = cls._construct_prefix(prefix)

        # Finds and creates the unit
        unit_str = unit if isinstance(unit, str) else ""
        unit_obj = cls._tokenize_unit(unit_str)

        return Factory.create(value, unit_obj, prefix)
