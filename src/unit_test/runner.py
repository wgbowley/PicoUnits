"""
File: runner.py

Description:
    Main script to run all unit test modules within
    the picounits library. This includes unit modelling, 
    parser, dynamic-loader and configurations.
"""

import unittest

from unit_test.unit.dimensional_algebra import DimensionAlgebra
from unit_test.unit.dimensional_construction import DimensionConstruction
from unit_test.quantities.quantities_construction import QualityScalingConstruction

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromTestCase(DimensionConstruction))
suite.addTests(loader.loadTestsFromTestCase(DimensionAlgebra))
suite.addTests(loader.loadTestsFromTestCase(QualityScalingConstruction))

runner = unittest.TextTestRunner(verbosity=2)

if __name__ == "__main__":
    result = runner.run(suite)
