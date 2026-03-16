"""
Filename: boundary_class
Author: William Bowley

Description:
    This blueprint serves as a boundary layer
    filter from typed units to raw values for
    fast operations.
"""

from abc import ABC, abstractmethod

from picounits import Quantity as Q


class UnitError(TypeError):
    """ Exception for Unit Error """
    def __init__(self, error: str):
        """ Returns a custom error message """
        msg = f"raised error: {error}. "
        super().__init__(msg)


class ValidBoundary(ABC):
    """ Serves as a boundary layer filter between unit values to raw values """
    def __init_subclass__(cls, **kwargs):
        """ Initialization wrapper for validation """
        super().__init_subclass__(**kwargs)
        original_init = cls.__init__

        def wrapped_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            self.validate_units()
            self.strip_units()

        cls.__init__ = wrapped_init

    def __setattr__(self, name: str, value) -> None:
        """ Intercepts all attribute setting, validates and strips if in requirements """
        requirements = (
            self.__class__.__dict__.get('_unit_requirements') or 
            getattr(self, '_unit_requirements', {})
        )

        if name in requirements:
            required_unit = requirements[name]

            if not isinstance(value, Q):
                msg = f"{name!r} must be a quantity, not {type(value)}"
                raise TypeError(msg)

            if value.unit != required_unit:
                msg = f"{name!r} must be {required_unit} not {value.unit}"
                raise UnitError(msg)

            super().__setattr__(name, float(value.stripped))
        else:
            super().__setattr__(name, value)

    @property
    @abstractmethod
    def _unit_requirements(self) -> dict:
        """ Returned units for initialization """
