"""
Filename: additional.py
Author: William Bowley
Version: 0.2

Description:
    Defines the methods for additional instance
    methods in Quantity via QuantityPacket

    NOTE: All these methods are logic methods
"""

from picounits.core.quantities.packet import QuantityPacket


def hashing_logic(q: QuantityPacket) -> int:
    """ Defines hashing behavior for standard quantity """
    return hash((q.magnitude, q.unit))
