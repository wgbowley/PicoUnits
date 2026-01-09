"""
Filename: priority.py
Author: William Bowley
Version: 0.1

Description:
    Builds the domain priority dictionary for
    factory.

    NOTE: Due to circular imports this dictionary
    has to be in a separate file and loaded in
    during Factory.reallocate() via lazy imports.
"""

from picounits.core.quantities.scalars.scalar import ScalarPacket
from picounits.core.quantities.vectors.vector import VectorPacket


DOMAIN_PRIORITY = {
    ScalarPacket: 1,
    VectorPacket: 2,
    # Add new ones here - just assign the Arithmetic Router
}
