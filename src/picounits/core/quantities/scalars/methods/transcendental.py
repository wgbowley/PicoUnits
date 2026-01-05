"""
Filename: transcendental.py
Author: William Bowley
Version: 0.2

Description:
    Defines the methods for transcendental mathematical
    functions methods for scalar quantities
"""

from picounits.core.unit import Unit
from picounits.core.quantities.packet import Packet


def _valid_input_for_transcendental(q: Packet, method: str) -> None:
    """ if unit is not dimensionless, it raises a value error """
    if q.unit is Unit.dimensionless():
        return None

    msg = (
        f"Methods '{method}' requires non-dimensionless Quantity, "
        f"{q.unit} != {Unit.dimensionless()}"
    )
    raise ValueError(msg)
