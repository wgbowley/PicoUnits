"""
File: unit_tests.py
Author: William Bowley
Version: 0.1

Description:
    Tests the 'Quantity' dataclass
    and its subclasses 'Unit', 'PreFixScale',
    'SIBase' and 'Dimension'
"""

import unittest

from math import sqrt, sin, pi
from picounits.dimensions.units import (
    Unit, Dimension, SIBase, PrefixScale, conversion,
    _valid_conversion
)


class UnitTest(unittest.TestCase):
    """
    Performs tests for the 'Unit' and its subclasses 'PreFixScale',
    'SIBase' and 'Dimension'
    """

    def test_prefix_scale_representation(self) -> None:
        """ Tests the representation of PrefixScale"""
        scale = PrefixScale.TERA

        expected = str("<Prefix.TERA: 10^12>")
        self.assertEqual(repr(scale), expected)

    def test_si_base_representation(self) -> None:
        """ Tests the representation of SIBase """
        base = SIBase.AMPERE

        expected = str("<SIBase.AMPERE>")
        self.assertEqual(repr(base), expected)

    def test_dimensional_correctness(self) -> None:
        """ Testing that the dimension inputs are correct"""
        with self.assertRaises(ValueError):
            # Non-PreFixScale type
            _ = Dimension("Scale? Whats that?")

        with self.assertRaises(ValueError):
            # Non-SIBase type
            _ = Dimension(base="SI Metric? Nah ImperialBase?")

        with self.assertRaises(ValueError):
            # Non-integer type for exponent
            _ = Dimension(exponent=67.67)

    def test_power_zero_cancel_of_base(self) -> None:
        """ Tests to ensure that bases to power of zero cancel """
        dim = Dimension(base=SIBase.MOLE, exponent=0)

        expected_base, expected_exponent = SIBase.DIMENSIONLESS, 1
        self.assertEqual(dim.base, expected_base)
        self.assertEqual(dim.exponent, expected_exponent)

    def test_dimension_representation(self) -> None:
        """ Tests the representation of a dimension """
        dim = Dimension(PrefixScale.CENTI, SIBase.CANDELA)

        expected = str("<Dimension name='ccd'>")
        self.assertEqual(expected, repr(dim))

    def test_empty_unit(self) -> None:
        """ Tests the dimensionally empty unit check """
        with self.assertRaises(RuntimeError):
            # Empty unit check
            _ = Unit()

    def test_non_dimension_in_unit(self) -> None:
        """ Test defining a unit with a non dimension """
        with self.assertRaises(ValueError):
            # Tries string
            _ = Unit(Dimension(base=SIBase.AMPERE), "I like Physics")

        with self.assertRaises(ValueError):
            # Tries integer
            _ = Unit(Dimension(base=SIBase.AMPERE), 420)

        with self.assertRaises(ValueError):
            # Tries float
            _ = Unit(Dimension(base=SIBase.AMPERE), 420.67)

        with self.assertRaises(ValueError):
            # Tries class (Enum)
            _ = Unit(Dimension(base=SIBase.AMPERE), SIBase.AMPERE)

    def test_standard_unit(self) -> None:
        """ Test the unit equality between same units """
        expected = Unit(Dimension(base=SIBase.AMPERE))
        result = Unit(
            Dimension(PrefixScale.BASE, base=SIBase.AMPERE, exponent=1)
        )
        self.assertEqual(expected, result)

    def test_zero_exponent_bases_normalize_to_same_unit(self) -> None:
        """
        Tests that units with different bases raised to the power of zero
        """
        meter_seconds_zero = Unit(
            Dimension(base=SIBase.METER),
            Dimension(base=SIBase.SECOND, exponent=0)
        )
        meter_kelvin_zero = Unit(
            Dimension(base=SIBase.METER),
            Dimension(base=SIBase.KELVIN, exponent=0)
        )

        meter_unit = Unit(Dimension(base=SIBase.METER))

        self.assertEqual(meter_kelvin_zero, meter_seconds_zero)
        self.assertEqual(meter_kelvin_zero, meter_unit)
        self.assertEqual(meter_seconds_zero, meter_unit)

    def test_standard_unit_hash(self) -> None:
        """ Tests the units objects are hashable and order independents """
        tesla_a = Unit(
            Dimension(PrefixScale.KILO, SIBase.GRAM),
            Dimension(base=SIBase.SECOND, exponent=-2),
            Dimension(base=SIBase.AMPERE, exponent=-1)
        )
        tesla_b = Unit(
            Dimension(base=SIBase.SECOND, exponent=-2),
            Dimension(base=SIBase.AMPERE, exponent=-1),
            Dimension(PrefixScale.KILO, SIBase.GRAM)
        )

        # Ensures Hashability (identical for keys)
        self.assertEqual(hash(tesla_a), hash(tesla_b))

        # Ensures that the unit can be used as a key
        unit_cache = {tesla_a: "Tesla Unit"}
        self.assertIn(tesla_b, unit_cache)

    def test_duplicated_si_bases(self) -> None:
        """ Test the unit duplicated bases logical """
        with self.assertRaises(RuntimeError):
            _ = Unit(
                Dimension(PrefixScale.KILO, SIBase.GRAM),
                Dimension(PrefixScale.KILO, SIBase.GRAM),
                Dimension(base=SIBase.SECOND, exponent=-2),
                Dimension(base=SIBase.AMPERE, exponent=-1)
            )

    def test_same_length_different_unit_valid_conversion(self) -> None:
        """ Test valid conversion helper function with different units """
        old_unit = Unit(Dimension(base=SIBase.KELVIN))
        new_unit = Unit(Dimension(PrefixScale.MEGA, SIBase.METER))

        with self.assertRaises(ValueError):
            _valid_conversion(old_unit, new_unit)

    def test_different_length_different_unit_valid_conversion(self) -> None:
        """
        Test valid conversion helper function with different length and unit
        """
        old_unit = Unit(
            Dimension(base=SIBase.CANDELA), Dimension(base=SIBase.KELVIN)
        )
        new_unit = Unit(Dimension(base=SIBase.MOLE))

        with self.assertRaises(ValueError):
            _valid_conversion(old_unit, new_unit)

    def test_same_length_complex_units_valid_conversion(self) -> None:
        """
        Test valid conversion helper function with same length & complex units
        """
        tesla = Unit(
            Dimension(PrefixScale.KILO, SIBase.GRAM),
            Dimension(base=SIBase.SECOND, exponent=-2),
            Dimension(base=SIBase.AMPERE, exponent=-1)
        )

        broken_tesla = Unit(
            Dimension(PrefixScale.MEGA, SIBase.GRAM),
            Dimension(base=SIBase.SECOND, exponent=-5),
            Dimension(base=SIBase.AMPERE, exponent=2)
        )

        with self.assertRaises(ValueError):
            _valid_conversion(tesla, broken_tesla)

    def test_base_to_kilo_unit_scaling(self) -> None:
        """
        Test unit scaling from prefix base to prefix kilo
        """
        old_unit = Unit(Dimension(PrefixScale.BASE, SIBase.CANDELA))
        new_unit = Unit(Dimension(PrefixScale.KILO, SIBase.CANDELA))
        magnitude = 10

        expected = 1e-2
        result, _ = conversion(magnitude, old_unit, new_unit)
        self.assertAlmostEqual(expected, result)

    def test_scaling_unit_with_one_as_exponent(self) -> None:
        """
        Test unit scaling between different prefixes with one as exponent
        """
        old_unit = Unit(Dimension(base=SIBase.AMPERE))
        new_unit = Unit(Dimension(PrefixScale.MEGA, SIBase.AMPERE))
        magnitude = 10

        expected = 1e-5
        result, _ = conversion(magnitude, old_unit, new_unit)
        self.assertAlmostEqual(expected, result)

    def test_inverse_scaling_with_one_as_exponent(self) -> None:
        """
        Test unit inverse scaling between different prefixes
        with one as exponent
        """
        old_unit = Unit(Dimension(PrefixScale.KILO, SIBase.METER))
        new_unit = Unit(Dimension(PrefixScale.BASE, SIBase.METER))
        magnitude = sqrt(2)

        expected = 1000*sqrt(2)
        result, _ = conversion(magnitude, old_unit, new_unit)
        self.assertAlmostEqual(expected, result)

    def test_scaling_unit_with_two_as_exponent(self) -> None:
        """
        Test unit scaling between different prefixes with two as exponent
        """
        old_unit = Unit(Dimension(PrefixScale.BASE, SIBase.KELVIN, 2))
        new_unit = Unit(Dimension(PrefixScale.NANO, SIBase.KELVIN, 2))
        magnitude = 3.2

        expected = 3.2e18
        result, _ = conversion(magnitude, old_unit, new_unit)
        self.assertAlmostEqual(expected, result)

    def test_scaling_unit_with_three_as_exponent(self) -> None:
        """
        Test unit scaling between different prefixes with three as exponent
        """
        old_unit = Unit(Dimension(PrefixScale.CENTI, SIBase.METER, 3))
        new_unit = Unit(Dimension(PrefixScale.MICRO, SIBase.METER, 3))
        magnitude = round(sin(pi/6), 3)

        expected = 5e11
        result, _ = conversion(magnitude, old_unit, new_unit)
        self.assertAlmostEqual(expected, result)

    def test_scaling_unit_with_negative_exponent(self) -> None:
        """ Test unit scaling with negative exponent """
        _meter_per_second = Unit(
            Dimension(PrefixScale.BASE, SIBase.METER),
            Dimension(PrefixScale.BASE, SIBase.SECOND, -1)
        )
        _meter_per_nanosecond = Unit(
            Dimension(PrefixScale.BASE, SIBase.METER),
            Dimension(PrefixScale.NANO, SIBase.SECOND, -1)
        )
        magnitude = 10

        expected = 1e-8
        result, _ = conversion(
            magnitude, _meter_per_second, _meter_per_nanosecond
        )
        self.assertAlmostEqual(expected, result)

    def test_scaling_unit_with_combined_units(self) -> None:
        """
        Test unit scaling between combined units with different prefixes
        """
        old_unit = Unit(
            Dimension(PrefixScale.KILO, SIBase.GRAM),
            Dimension(PrefixScale.NANO, SIBase.METER, exponent=2),
            Dimension(base=SIBase.SECOND, exponent=-3),
            Dimension(base=SIBase.AMPERE, exponent=-1)
        )
        new_unit = Unit(
            Dimension(PrefixScale.BASE, SIBase.GRAM),
            Dimension(PrefixScale.BASE, SIBase.METER, exponent=2),
            Dimension(base=SIBase.SECOND, exponent=-3),
            Dimension(base=SIBase.AMPERE, exponent=-1)
        )
        magnitude = 5

        expected = 5e-15
        result, _ = conversion(magnitude, old_unit, new_unit)
        self.assertAlmostEqual(expected, result)

    def test_scaling_unit_dimensionless_units(self) -> None:
        """ Test scaling unit with dimensionless units """
        old_unit = Unit(Dimension(PrefixScale.MEGA, SIBase.DIMENSIONLESS))
        new_unit = Unit(Dimension(PrefixScale.TERA, SIBase.DIMENSIONLESS))
        magnitude = 20

        expected = 2e-5
        result, _ = conversion(magnitude, old_unit, new_unit)
        self.assertAlmostEqual(expected, result)

    def test_scaling_unit_with_random_dimensionless_in_units(self) -> None:
        """ Tests scaling with random dimensionless parameters in units """
        _weber = Unit(
            Dimension(PrefixScale.KILO, SIBase.GRAM),
            Dimension(base=SIBase.METER, exponent=2),
            Dimension(PrefixScale.TERA, SIBase.DIMENSIONLESS),
            Dimension(base=SIBase.SECOND, exponent=-2),
            Dimension(base=SIBase.AMPERE, exponent=-1)
        )
        _weber_2 = Unit(
            Dimension(PrefixScale.NANO, SIBase.DIMENSIONLESS),
            Dimension(base=SIBase.GRAM),
            Dimension(base=SIBase.METER, exponent=2),
            Dimension(base=SIBase.SECOND, exponent=-2),
            Dimension(base=SIBase.AMPERE, exponent=-1)
        )
        magnitude = 4.5*pi

        expected = 4500*pi
        result, _ = conversion(magnitude, _weber, _weber_2)
        self.assertAlmostEqual(expected, result)

    def test_conversion_preserves_integers(self) -> None:
        """ Tests the converting while preserving integer values """
        old_unit = Unit(Dimension(PrefixScale.BASE, SIBase.METER))
        new_unit = Unit(Dimension(PrefixScale.KILO, SIBase.METER))

        # Exact integer conversion
        magnitude = 1000
        expected = 1
        result, _ = conversion(magnitude, old_unit, new_unit)
        self.assertEqual(result, expected)
        self.assertIsInstance(result, int)

        # Inexact float conversion
        magnitude = 1000.1
        expected = 1.0001
        result, _ = conversion(magnitude, old_unit, new_unit)
        self.assertEqual(result, expected)
        self.assertIsInstance(result, float)

    def test_unit_representation_method(self) -> None:
        """ Tests unit representation method """
        _permeability = Unit(
            Dimension(PrefixScale.KILO, SIBase.GRAM),
            Dimension(base=SIBase.METER),
            Dimension(base=SIBase.SECOND, exponent=-2),
            Dimension(base=SIBase.AMPERE, exponent=-2)
        )

        expected = str("kg m s^-2 A^-2")
        representation = str(_permeability.name)
        self.assertEqual(expected, representation)

    def test_unit_representation_method_dimensionless_in_unit(self) -> None:
        """ Tests unit representation method when dimensionless in unit """
        _weber = Unit(
            Dimension(PrefixScale.KILO, SIBase.GRAM),
            Dimension(base=SIBase.METER, exponent=2),
            Dimension(PrefixScale.TERA, SIBase.DIMENSIONLESS),
            Dimension(base=SIBase.SECOND, exponent=-2),
            Dimension(base=SIBase.AMPERE, exponent=-1)
        )

        expected = str("kg m^2 s^-2 A^-1")
        representation = str(_weber.name)
        self.assertEqual(expected, representation)

    def test_dimensionless_representation_method(self) -> None:
        """ Tests unit representation of dimensionless unit """
        _radians = Unit(Dimension(base=SIBase.DIMENSIONLESS))

        expected = str("∅")
        representation = str(_radians.name)
        self.assertEqual(expected, representation)
