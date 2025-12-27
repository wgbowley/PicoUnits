"""
Filename: function.py
Author: William Bowley
Version: 0.1

Description:
    Defines the Mixin for mathematical functions
    and properties under 'FunctionsMixin'

    NOTE:
    Due to implementation structure methods cannot be typed hinted
    but a general rule is that if it mutates, its a new Quantity
"""

from math import radians, degrees, sin, cos, tan, exp, log

from picounits.constants import DIMENSIONLESS


class FunctionsMixin:
    """ Contains the mathematical functions build into python """

    """ Angles methods"""
    def to_radians(self):
        """ Converts the Quantity to radians, if dimensionless """
        if self.unit is DIMENSIONLESS:
            origin_based = self.to_base()
            magnitude = radians(origin_based.magnitude)

            return self.__class__(magnitude, DIMENSIONLESS)

        msg = f"Cannot convert to radians as {self.unit} != {DIMENSIONLESS}"
        raise ValueError(msg)

    def to_degrees(self):
        """ Converts the Quantity to degrees, if dimensionless """
        if self.unit is DIMENSIONLESS:
            origin_based = self.to_base()
            magnitude = degrees(origin_based.magnitude)

            return self.__class__(magnitude, DIMENSIONLESS)

        msg = f"Cannot convert to degrees as {self.unit} != {DIMENSIONLESS}"
        raise ValueError(msg)

    """ Trigonometry methods """
    def sin(self):
        """ Performs the sine operation, if dimensionless """
        if self.unit is DIMENSIONLESS:
            origin_based = self.to_base()
            magnitude = sin(origin_based.magnitude)

            return self.__class__(magnitude, DIMENSIONLESS)

        msg = f"Cannot perform sine as {self.unit} != {DIMENSIONLESS}"
        raise ValueError(msg)

    def cos(self):
        """ Performs the cosine operation, if dimensionless """
        if self.unit is DIMENSIONLESS:
            origin_based = self.to_base()
            magnitude = cos(origin_based.magnitude)

            return self.__class__(magnitude, DIMENSIONLESS)

        msg = f"Cannot perform cosine as {self.unit} != {DIMENSIONLESS}"
        raise ValueError(msg)

    def tan(self):
        """ Performs the tangent operation, if dimensionless """
        if self.unit is DIMENSIONLESS:
            origin_based = self.to_base()
            magnitude = tan(origin_based.magnitude)

            return self.__class__(magnitude, DIMENSIONLESS)

        msg = f"Cannot perform tangent as {self.unit} != {DIMENSIONLESS}"
        raise ValueError(msg)

    """ Exponential Methods"""
    def exp(self):
        """ Preforms the exponential operation, if dimensionless """
        if self.unit is DIMENSIONLESS:
            origin_based = self.to_base()
            magnitude = exp(origin_based.magnitude)

            return self.__class__(magnitude, DIMENSIONLESS)

        msg = f"Cannot perform exp as {self.unit} != {DIMENSIONLESS}"
        raise ValueError(msg)

    def nlog(self):
        """ Preforms the natural logarithm, if dimensionless """
        if self.unit is DIMENSIONLESS:
            origin_based = self.to_base()
            magnitude = log(origin_based.magnitude)

            return self.__class__(magnitude, DIMENSIONLESS).normalized()

        msg = f"Cannot perform nlog as {self.unit} != {DIMENSIONLESS}"
        raise ValueError(msg)
