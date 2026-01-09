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

from typing import Any, Callable

from picounits.core.quantities.packet import Packet

from picounits.lazy_imports import lazy_import

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
            prefixscale = lazy_import(
                "picounits.core.scales", "PrefixScale", "Factory.create"
            )
            prefix = prefixscale.BASE

        match value:
            case complex():
                complex_packet = lazy_import(
                    "picounits.core.quantities.scalars.types.complex", 
                    "ComplexPacket", "Factory.create"
                )

                return complex_packet(value, unit, prefix)

            case float() | int():
                real_packet = lazy_import(
                    "picounits.core.quantities.scalars.types.real", 
                    "RealPacket", "Factory.create"
                )
                return real_packet(value, unit, prefix)

            case tuple() | list():
                array_packet = lazy_import(
                    "picounits.core.quantities.vectors.types.array_vector",
                    "ArrayPacket", "Factory.create"
                )
                return array_packet(value, unit, prefix)

            case _:
                msg = f"No Packet for this value type: {type(value)}"
                raise TypeError(msg)

    @classmethod
    def reallocate(cls, op_name: str) -> Callable:
        """
        Reallocate arithmetic or transcendental methods when packets are
        not similar types. For example ScalarPacket != VectorPacket
        """

        def decorator(method: Callable) -> Callable:
            def wrapper(q1: Packet, q2: Packet) -> Callable:
                """ Promotes methods if they dont have the same parents """
                q1_parents = q1.__class__.__bases__[0]
                q2_parents = q2.__class__.__bases__[0]
                if q1_parents == q2_parents:
                    # Simple pass through if same class has the same parent
                    return method(q1, q2)

                # Initialization due to circular import of literals
                domain_priority = lazy_import(
                    "picounits.core.quantities.priority",
                    "DOMAIN_PRIORITY", "Factory.reallocate"
                )

                # Gets priority of each packet_type
                p1 = domain_priority.get(q1_parents, 0)
                p2 = domain_priority.get(q2_parents, 0)

                # Finds the native operator for these packets
                winner = q1 if p1 >= p2 else q2
                loser = q2 if winner is q1 else q1

                # Reallocate this result to another arithmetic router
                return getattr(winner, op_name)(loser)
            return wrapper
        return decorator
