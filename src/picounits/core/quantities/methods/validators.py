"""
Filename: validators.py
Author: William Bowley
Version: 0.1

Description:
    Defines the methods for unit and arithmetic validators
    methods in Quantity & CQuantity via VPacket

    NOTE: All these methods are logic methods
"""

from typing import Callable

from picounits.core.unit import Unit
from picounits.core.quantities.vpacket import VPacket


def _check_quantity(q: VPacket, wrapper: str) -> None:
    """ Checks to ensure q is a quantity """
    if isinstance(q, VPacket):
        return

    msg = f"{wrapper} returned {type(q)}, expected Quantity"
    raise TypeError(msg)


def _check_forecasted(u1: Unit, u2: Unit, wrapper: str) -> None:
    """ Checks to ensure u1 is equal to u2 """
    if isinstance(u1, Unit) and isinstance(u2, Unit):
        if u1 == u2:
            return

    msg = f"{wrapper.__name__} returned {u1}, expected {u2}"
    raise ValueError(msg)


def check_unit_output(forecasted: Unit) -> Callable:
    """
    A decorator; it checks a function unit output, if different raises an error
    """
    def decorator(func) -> Callable:
        def wrapper(*args, **kwargs) -> Callable:
            result = func(*args, **kwargs)

            # Single Quantity
            if isinstance(result, VPacket):
                _check_forecasted(result.unit, forecasted, wrapper.__name__)
                return result

            # Tuple or list of Quantities
            if isinstance(result, (tuple, list)):
                for item in result:
                    _check_quantity(item, wrapper.__name__)
                    _check_forecasted(
                        item.unit, forecasted, wrapper.__name__
                    )
                return result

            msg = (
                f"{func.__name__} returned {type(result)}, "
                "expected Quantity or tuple/list of Quantity"
            )
            raise TypeError(msg)

        return wrapper
    return decorator
