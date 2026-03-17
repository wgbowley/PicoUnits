"""
Filename: dimensional_algebra.py
Author: William Bowley

Description:
    Tests for the Unit class to ensure that the 
    dimensional algebra and pipelines are correct.
    
    NOTE:
    Testing for string representation should be added.
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

    def test_dimensionless_factory(self):
        """ Factory method for dimensionless outputs """
        dimensionless_via_factory = Unit.dimensionless()
        dimensionless_via_construction = Unit(_DIMENSIONLESS)

        self.assertEqual(
            dimensionless_via_construction, dimensionless_via_factory
        )

    def test_unit_forwards_multiplication(self):
        """ Tests multiplication different units together """
        cases = [
            ((Unit(_LENGTH), Unit(_TIME)), Unit(_LENGTH, _TIME)),
            ((Unit(_MASS), Unit(_TIME)), Unit(_MASS, _TIME)),
            ((Unit(_CURRENT), Unit(_MASS)), Unit(_CURRENT, _MASS)),
            ((Unit(_AMOUNT), Unit(_LUMINOSITY)), Unit(_LUMINOSITY, _AMOUNT)),
            (
                (Unit(_MASS), Unit(Dimension(FBase.CURRENT, 2))),
                Unit(_MASS, Dimension(FBase.CURRENT, 2))
            ),
            (
                (Unit(_MASS), Unit(_MASS)), Unit(Dimension(FBase.MASS, 2))
            )
        ]

        for case in cases:
            units, expected = case
            result = units[0] * units[1]

            self.assertEqual(result.dimensions, expected.dimensions)

    def test_unit_forwards_true_division(self):
        """ Tests true division between different units """
        cases = [
            (
                (Unit(_DIMENSIONLESS), Unit(_TEMPERATURE)),
                Unit(Dimension(FBase.TEMPERATURE, -1))
            ),
            (
                (Unit(_TEMPERATURE), Unit(_AMOUNT)),
                Unit(Dimension(FBase.AMOUNT, -1), _TEMPERATURE)
            ),
            (
                (Unit(_MASS), Unit(Dimension(FBase.CURRENT, 2))),
                Unit(_MASS, Dimension(FBase.CURRENT, -2))
            ),
            (
                (1, Unit(_MASS)), # Reciprocal of the unit (edge case)
                Unit(Dimension(FBase.MASS, -1))
            )
        ]

        for case in cases:
            units, expected = case
            results = units[0] / units[1]

            self.assertEqual(results.dimensions, expected.dimensions)

    def test_unit_backwards_true_division(self):
        """ Tests true division between a unit and different value """
        with self.assertRaises(ValueError):
            _ = Unit(_MASS) / 10

    def test_unit_forwards_power(self):
        """ Tests power between a unit and a integer or float """
        cases = [
            ((Unit(_LENGTH), 1), Unit(_LENGTH)),
            ((Unit(_MASS), -2), Unit(Dimension(FBase.MASS, -2))),
            ((Unit(_LENGTH), 10.0), Unit(Dimension(FBase.LENGTH, 10))),
            ((Unit(_CURRENT), 0.1), Unit(Dimension(FBase.CURRENT, 0.1))),
            ((Unit(_TIME), -0.1), Unit(Dimension(FBase.TIME, -0.1)))
        ]

        for case in cases:
            units, expected = case
            results = units[0] ** units[1]

            self.assertEqual(results.dimensions, expected.dimensions)

    def test_unit_backwards_power(self):
        """ Tests backwards power between a number and a unit """
        with self.assertRaises(TypeError):
            _ = 1 ** Unit(_TEMPERATURE)

if __name__ == '__main__':
    unittest.main(verbosity=2)
