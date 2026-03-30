"""
Filename: factory.pyi
Author: William Bowley
Version: 0.1
Clear: X

Description:
    Static type hinting for the factory module.
    The factory is type caster for quantities and
    dispatcher for mathematical methods
"""

from numpy import ndarray, integer, floating, complexfloating

from typing import Callable, overload
from picounits.core.unit import Unit
from picounits.core.scales import PrefixScale
from picounits.core.quantities.scalars.types.complex import ComplexPacket
from picounits.core.quantities.scalars.types.real import RealPacket
from picounits.core.quantities.vectors.types.array import ArrayPacket


class Factory:
    @overload
    @classmethod
    def create(
        cls, value: complex | complexfloating, unit: Unit, prefix: PrefixScale | None = None
    ) -> ComplexPacket: ...

    @overload
    @classmethod
    def create(
        cls, value: float | int | floating | integer, prefix: PrefixScale | None = None
    ) -> RealPacket: ...

    @overload
    @classmethod
    def create(
        cls, value: ndarray | list | tuple, prefix: PrefixScale | None = None
    ) -> ArrayPacket: ...

    @classmethod
    def create(
        cls, 
        value: complex | float | int | floating | ndarray | list | tuple | integer | complexfloating,
        unit: Unit,
        prefix: PrefixScale | None = None,
    ) -> ComplexPacket | RealPacket | ArrayPacket: ...

    @classmethod
    def reallocate(cls, op_name: str) -> Callable[[Callable], Callable]: ... 
    
    @classmethod
    def category_check(cls, q1: Packet, q2: Packet) -> None: ...