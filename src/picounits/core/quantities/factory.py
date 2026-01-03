"""
Filename: factory.py
Author: William Bowley
Version: 0.1
Clear: X

Description:
    Defines the Quantity Factory Class, acts
    as a type caster for quantities within
    the agnostic functional endpoint methods.
"""

from typing import Any

from picounits.core.quantities.packet import Packet


class Factory:
    """
    Packet type casing factory for usage in agnostic functional methods
    """
    @classmethod
    def create(cls, value: Any, unit, prefix=None) -> Packet:
        """
        Finds the type of the value and returns a casted packet
        NOTE: The usage of import injection is to avoid circular imports
        NOTE: Cannot type hint unit nor prefix due to circular imports
        """
        if prefix is None:
            from picounits.core.scales import PrefixScale
            prefix = PrefixScale.BASE

        match value:
            case complex():
                from picounits.core.quantities.types.complex import (
                    ComplexPacket
                )
                return ComplexPacket(value, unit, prefix)

            case float() | int():
                from picounits.core.quantities.types.real import (
                    RealPacket
                )
                return RealPacket(value, unit, prefix)

            case _:
                msg = f"No Packet for this value type: {type(value)}"
                raise TypeError(msg)
