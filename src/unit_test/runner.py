# pylint: skip-file
"""
File: runner.py

Description:
    Main script to run all unit test modules within
    the picounits library. This includes unit modelling, 
    parser, dynamic-loader and configurations.
    
    NOTE: Reference commands:
    coverage run src/unit_test/runner.py
    coverage report -m
"""

import unittest

from unit.dimensional_algebra import DimensionAlgebra
from unit.dimensional_construction import DimensionConstruction
from quantities.quantities_construction import QualityScalingConstruction

from parser.core import TestParseList, TestDeserialize

loader = unittest.TestLoader()
suite = unittest.TestSuite()

# Core
suite.addTests(loader.loadTestsFromTestCase(DimensionConstruction))
suite.addTests(loader.loadTestsFromTestCase(DimensionAlgebra))
suite.addTests(loader.loadTestsFromTestCase(QualityScalingConstruction))

# Extensions
suite.addTests(loader.loadTestsFromTestCase(TestParseList))
suite.addTests(loader.loadTestsFromTestCase(TestDeserialize))

runner = unittest.TextTestRunner(verbosity=2)

if __name__ == "__main__":
    result = runner.run(suite)
