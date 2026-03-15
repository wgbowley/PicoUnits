"""
Filename: dimensional_construction.py
Author: William Bowley

Description:
    Tests for the fundamental unit 'FBASE' and dataclass 'Dimension'
    to ensure that the dimensional construction is correct for the application.
"""

import unittest
from picounits.core.dimensions import Dimension, FBase, SUPERSCRIPT_MAP


class DimensionConstruction(unittest.TestCase):
    """ Tests dimensional construction system"""
    def test_construct_dimensions(self):
        """ Construct a dimension with each known base unit """
        for base in FBase:
            _ = Dimension(base, 1)

    def test_construction_with_non_Fbase(self):
        """ Non-valid construction without Fbase """
        invalid_cases = ["MASS", [FBase.AMOUNT], {}, 10, 0.1]

        for base in invalid_cases:
            with self.assertRaises(TypeError):
                Dimension(base, 1)

    def test_construction_with_non_numerical_exponent(self):
        """ Non-valid construction with non float or integer exponent """
        invalid_cases = [
            (FBase.AMOUNT, "Im non-numerical"),
            (FBase.MASS, [10, 10, 10]),
            (FBase.LENGTH, {})
        ]

        for base, exponent in invalid_cases:
            with self.assertRaises(TypeError):
                Dimension(base, exponent)

    def test_construct_dimensionless(self):
        """ Construct of dimensionless via x^0=1 or redefining exponent to 1 """
        zero_exponent = Dimension(FBase.LENGTH, 0)
        redefined_to_one = Dimension(FBase.DIMENSIONLESS, 10)

        # Zero exponent should return base of dimensionless and exponent of 1
        self.assertIs(zero_exponent.base, FBase.DIMENSIONLESS)
        self.assertEqual(zero_exponent.exponent, 1)

        # Redefined to one should mutate exponent from 10 to 1
        self.assertEqual(redefined_to_one.exponent, 1)

    def test_integer_float_and_fractional_superscripts(self):
        """ Construct of dimensions with integer, float and fractional superscripts """
        def _convert_to_unicode(superscript: str) -> str:
            """ Converts to unicode from ascii """
            return superscript.translate(SUPERSCRIPT_MAP)

        base_cases = [
            (1, "1"), (1/2, "1/2"), (1/18, "1/18"), (-1, "-1"), (-1/5, "-1/5"),
            (0.1, "1/10"), (0.05, "1/20"), (10, "10"), (1/2500, "1/2500"), (2.0, "2")
        ]

        for exponent, expected in base_cases:
            dim = Dimension(FBase.MASS, exponent)
            superscript = dim.superscript

            self.assertEqual(superscript, _convert_to_unicode(expected))

    def test_dimensionless_factory(self):
        """ Factory method for dimensionless outputs """
        dim = Dimension.dimensionless()
        self.assertEqual(dim, Dimension(FBase.DIMENSIONLESS, 1))

if __name__ == '__main__':
    unittest.main()
