"""
Filename: validators.py
Author: William Bowley
Version: 0.2
Clear: X

Description:
    Defines the methods for the unit validator
    method in the Packet ABC dataclass
"""

from typing import Callable

from picounits.core.unit import Unit
from picounits.core.quantities.packet import Packet

# Easy reference for users
Quantity = Packet


class DimensionError(ValueError):
    """ Exception for unit error """
    def __init__(self, caller: str, message: str):
        """ Returns a custom error message for unit error """
        msg = f"{caller!r} {message}"
        super().__init__(msg)


def _check_packet(q: Packet, func: str) -> None:
    """ Checks to ensure q is a packet """
    if isinstance(q, Packet):
        return

    msg = f"returned {type(q)}, expected packet"
    raise DimensionError(func, msg)


def _check_forecasted(u1: Unit, u2: Unit, func: str) -> None:
    """ Checks to ensure u1 is equal to u2 """
    if isinstance(u1, Unit) and isinstance(u2, Unit):
        if u1 == u2:
            return

    msg = f"returned {u1}, expected {u2}"
    raise DimensionError(func, msg)


def unit_validator(forecasted: Unit) -> Callable:
    """
    A decorator; it checks a function unit output, if different raises an error
    """
    def decorator(func) -> Callable:
        def wrapper(*args, **kwargs) -> Callable:
            result = func(*args, **kwargs)

            # Single Packet
            if isinstance(result, Packet):
                _check_forecasted(result.unit, forecasted, func.__name__)
                return result

            # Tuple or list of Packets
            if isinstance(result, (tuple, list)):
                for item in result:
                    _check_packet(item, func.__name__)
                    _check_forecasted(
                        item.unit, forecasted, func.__name__
                    )
                return result

            msg = (
                f"{func.__name__} returned {type(result)}, "
                "expected Packet or tuple/list of Packets"
            )
            raise TypeError(msg)

        return wrapper
    return decorator
