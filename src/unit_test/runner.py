"""
File: runner.py
Author: William Bowley

Description:
    Main script to run all unit test modules within
    the picounits library. This includes unit modelling, 
    parser, dynamic-loader and configurations.
"""

import unittest

from unit_test.unit.dimensional_algebra import DimensionAlgebra
from unit_test.unit.dimensional_construction import DimensionConstruction


loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromTestCase(DimensionConstruction))
suite.addTests(loader.loadTestsFromTestCase(DimensionAlgebra))


runner = unittest.TextTestRunner(verbosity=2)

if __name__ == "__main__":
    result = runner.run(suite)
