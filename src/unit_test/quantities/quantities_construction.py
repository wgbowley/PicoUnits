"""
Filename: qualities_construction.py

Descriptions:
    Tests the scaling and construction of Qualities with a
    focus on prefix-exponent interactions 
"""

import unittest
from picounits import MILLI, KILO, LENGTH, TIME, MASS

class QualityScalingConstruction(unittest.TestCase):
    """Tests the scaling logic during construction of unit-informed values"""

    def test_linear_prefix_scaling(self):
        """Tests standard linear scaling (exponent = 1) for base units"""
        for exp in range(-100, 101):
            test_val = 1.0
            quality = test_val * MILLI * (LENGTH ** exp)

            expected_value = (test_val * 10 ** -3)
            self.assertAlmostEqual(
                quality.value,
                expected_value,
                msg=f"Failed scaling at exponent: {exp}"
            )

    def test_squared_prefix_scaling(self):
        """Tests squared scaling (exponent = 2) for area-based units #7"""
        milli_meter_sq = 10 * MILLI * (LENGTH ** 2)
        self.assertAlmostEqual(milli_meter_sq.value, 0.01)

    def test_cubic_prefix_scaling(self):
        """Tests cubic scaling (exponent = 3) for volume-based units"""
        kilo_meter_cu = 1 * KILO * (LENGTH ** 3)
        self.assertEqual(kilo_meter_cu.value, 1000)

    def test_inverse_scaling_behavior(self):
        """Tests scaling for units with negative exponents (e.g., Frequency)"""
        inv_milli_second = 1 * MILLI * (TIME ** -1)
        self.assertAlmostEqual(inv_milli_second.value, 0.001)

    def test_composite_unit_scaling_limit(self):
        """Ensures that scaling applies correctly to single-dimension units"""
        milli_mass_area = 1 * MILLI * MASS * (LENGTH ** 2)
        self.assertAlmostEqual(milli_mass_area.value, 0.001)

    def test_zero_exponent_scaling(self):
        """Tests that dimensionless construction (exponent 0) doesn't break scaling"""
        dimensionless = 10 * MILLI * (LENGTH ** 0)
        self.assertAlmostEqual(dimensionless.value, 0.010)

if __name__ == '__main__':
    unittest.main()