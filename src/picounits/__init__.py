# pylint: skip-file
# picounits/__init__.py

from typing import Any

from picounits.extensions.parser import Parser
from picounits.extensions.loader import DynamicLoader

from picounits.constants import *
from picounits.core.quantities.validators import unit_validator, Quantity
from picounits.configuration.config import reload_config

# Reloads the users .picounits configuration file.
reload_config()

# References for quantities when doing type hinting.
Q, q = Quantity, Quantity
_ = unit_validator

# Parser & Loader import
_ = Parser
_ = DynamicLoader


class UnitError(TypeError):
    """ Exception for Unit Error """
    def __init__(self, error: str, messenger: str |  None = None):
        """ Returns a custom error message """
        if messenger:
            msg = f"{messenger!r} raised error: {error}."
        else:
            msg = f"Unit error occurred: {error}."
        super().__init__(msg)


def check_quantity(quantity: Quantity, ref: Quantity) -> None:
    """ Checks if the quantity has the correct reference unit """
    if not isinstance(quantity, Quantity):
        msg = f"{type(quantity)!r} is not a physical quantity object"
        raise UnitError(msg)

    if not isinstance(ref, (Unit, Quantity)):
        msg = f"Reference unit must be either a quantity or unit, not {type(ref)}"
        raise UnitError(msg)

    if isinstance(ref, Quantity):
        if quantity.unit != ref.unit:
            msg = f"Expected {ref.unit!r}, got {quantity.unit!r}"
            raise UnitError(msg)

    if isinstance(ref, Unit):
        if quantity.unit != ref:
            msg = f"Expected {ref!r}, got {quantity.unit!r}"
            raise UnitError(msg)


def strip_quantity(quantity: Quantity, reference: Quantity) -> Any:
    """ Strips quantity from value returns raw value """
    check_quantity(quantity, reference)

    return quantity.value
