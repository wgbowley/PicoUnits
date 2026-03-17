"""
Filename: dimensional_algebra.py
Author: William Bowley

Description:
    Tests for the Unit class to ensure that the 
    dimensional algebra and pipelines are correct.
"""

import unittest
from picounits.core.dimensions import Dimension, FBase
from picounits.core.unit import Unit

# Defining fundamental dimensions

_TIME           = Dimension(base=FBase.TIME)
_LENGTH         = Dimension(base=FBase.LENGTH)
_MASS           = Dimension(base=FBase.MASS)
_CURRENT        = Dimension(base=FBase.CURRENT)
_TEMPERATURE    = Dimension(base=FBase.TEMPERATURE)
_AMOUNT         = Dimension(base=FBase.AMOUNT)
_LUMINOSITY     = Dimension(base=FBase.LUMINOSITY)
_DIMENSIONLESS  = Dimension(base=FBase.DIMENSIONLESS)


class DimensionAlgebra(unittest.TestCase):
    """ Tests dimensional algebra system """
    def test_construct_units(self):
        """ Constructs each fundamental unit """
        fundamental = []
        for base in FBase:
            fundamental.append(Dimension(base))

        for dim in fundamental:
            _ = Unit(dim)

    def test_non_Dimension_construction(self):
        """ Tests invalid construction via using float, int, etc """
        cases = ["mass", 10.1, 1, -1, {}, []]

        for dim in cases:
            with self.assertRaises(ValueError):
                _ = Unit(dim)

    def test_removal_of_duplicated_bases(self):
        """ Removal of duplicated bases """
        mass = Dimension(FBase.MASS)

        with self.assertRaises(ValueError):
            _ = Unit(mass, mass)

    def test_removal_of_dimensionless(self):
        """ Tests removal of dimensionless """
        length = Dimension(FBase.LENGTH)
        dimensionless = Dimension.dimensionless()

        unit = Unit(length, dimensionless)
        self.assertEqual(unit.dimensions, [length])

    def test_times_units(self):
        """ Tests timing different units together """
        cases = [
            ((Unit(_LENGTH), Unit(_TIME)), Unit(_LENGTH, _TIME)),
            ((Unit(_MASS), Unit(_TIME)), Unit(_MASS, _TIME)),
            ((Unit(_CURRENT), Unit(_MASS)), Unit(_CURRENT, _MASS)),
            ((Unit(_AMOUNT), Unit(_LUMINOSITY)), Unit(_LUMINOSITY, _AMOUNT)),
        ]

        for case in cases:
            units, expected = case
            result = units[0] * units[1]

            self.assertEqual(result.dimensions, expected.dimensions)

if __name__ == '__main__':
    unittest.main()
