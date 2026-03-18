"""
Filename: boundary_class
Author: William Bowley

Description:
    This blueprint serves as a boundary layer
    filter from typed units to raw values for
    fast operations.
"""

from abc import ABC, abstractmethod
from dataclasses import fields

from picounits import Quantity as Q


class UnitError(TypeError):
    """ Exception for Unit Error """
    def __init__(self, error: str):
        """ Returns a custom error message """
        msg = f"raised error: {error}. "
        super().__init__(msg)


class ValidBoundary(ABC):
    """ Unit boundary checking for dataclass construction""" 
    def validate_units(self) -> None:
        """ Generic validator that uses field metadata """
        for f in fields(self):
            required_unit = f.metadata.get(Q)
            if required_unit is None:
                continue

            attribute = getattr(self, f.name)
            if attribute is None:
                return

            if not isinstance(attribute, Q):
                msg = f"{f.name!r} must be a quantity, not {type(attribute)}"
                raise TypeError(msg)

            if attribute.unit != required_unit:
                msg = f"{f.name!r} must be {required_unit} not {attribute.unit}"
                raise UnitError(msg)

    @property
    @abstractmethod
    def _name(self) -> str:
        """ Constructs a name based on attributes """

    def __post_init__(self) -> None:
        """ Pipes users input variables into validation schema """
        self.validate_units()

    def __repr__(self) -> str:
        """ Returns the dataclasses name """""
        return self._name

    def __str__(self) -> str:
        """ Returns the dataclasses name """
        return self._name
