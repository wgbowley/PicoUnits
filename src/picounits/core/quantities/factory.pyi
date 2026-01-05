"""
Filename: factory.py
Author: William Bowley
Version: 0.1
Clear: X

Description:
    Static type hinting for the factory module.
    The factory is type caster for quantities and
    dispatcher for mathematical methods
"""

from typing import Callable, overload
from picounits.core.unit import Unit
from picounits.core.scales import PrefixScale
from picounits.core.quantities.scalars.types.complex import ComplexPacket
from picounits.core.quantities.scalars.types.real import RealPacket


class Factory:
    @overload
    @classmethod
    def create(
        cls, value: complex, unit: Unit, prefix: PrefixScale | None = None
    ) -> ComplexPacket: ...

    @overload
    @classmethod
    def create(
        cls, value: float | int, prefix: PrefixScale | None = None
    ) -> RealPacket: ...

    @classmethod
    def create(
        cls, 
        value: complex | float | int, 
        unit: Unit, 
        prefix: PrefixScale | None = None
    ) -> ComplexPacket | RealPacket: ...

    @classmethod
    def reallocate(cls, op_name: str) -> Callable[[Callable], Callable]: ...