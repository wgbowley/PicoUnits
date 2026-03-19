""" picounits/__init__.py """

from picounits.constants import *
from picounits.core.quantities.scalars.methods.validators import (
    unit_validator, Quantity
)

Q = Quantity


class UnitError(TypeError):
    """ Exception for Unit Error """
    def __init__(self, error: str):
        """ Returns a custom error message """
        msg = f"raised error: {error}. "
        super().__init__(msg)
