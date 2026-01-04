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
            try:
                # Provides a custom error message for the import injection
                from picounits.core.scales import PrefixScale
            except ImportError as error:
                msg = (
                    "Could not import 'PrefixScale' for Factory.create"
                    "This usually means picounits was not installed correctly "
                )
                raise ImportError(msg) from error

            prefix = PrefixScale.BASE

        match value:
            case complex():
                from picounits.core.quantities.scalars.types.complex import (
                    ComplexPacket
                )
                return ComplexPacket(value, unit, prefix)

            case float() | int():
                from picounits.core.quantities.scalars.types.real import (
                    RealPacket
                )
                return RealPacket(value, unit, prefix)

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
                try:
                    from picounits.core.quantities.priority import (
                        DOMAIN_PRIORITY
                    )
                except ImportError as error:
                    msg = (
                        "Could not import 'DOMAIN_PRIORITY' for "
                        "Factory.reallocate. This usually means "
                        "picounits was not installed correctly"
                    )
                    raise ImportError(msg) from error

                # Gets priority of each packet_type
                p1 = DOMAIN_PRIORITY.get(q1_parents, 0)
                p2 = DOMAIN_PRIORITY.get(q2_parents, 0)

                # Finds the native operator for these packets
                winner = q1 if p1 >= p2 else q2
                loser = q2 if winner is q1 else q1

                # Reallocate this result to another arithmetic router
                return getattr(winner, op_name)(loser)
            return wrapper
        return decorator