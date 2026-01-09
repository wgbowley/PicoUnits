"""
Filename: vectors.py
Author: William Bowley
Version: 0.1
Clear: X

Description:
    Defines the semi-abstract VectorPacket Class
    which is defines arithmetic routing for vector
    but not representation or prefix scaling
"""

from typing import Any
from abc import ABC
from dataclasses import dataclass

from picounits.core.unit import Unit
from picounits.core.quantities.packet import Packet
from picounits.core.quantities.factory import Factory


from picounits.lazy_imports import import_factory


@dataclass(slots=True)
class VectorPacket(Packet, ABC):
    """
    An Abstract Vector Packet: A prefix, value (Any Vector) and Unit

    NOTE: Representation, prefix scaling, comparison, validation
    are not implemented in this base case.
    """
