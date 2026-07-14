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

from unit_test.parser.core.deserialization import TestParseList, TestDeserialize
from unit_test.parser.utilities.operations import TestOperators

loader = unittest.TestLoader()
suite = unittest.TestSuite()

# === Core ===

suite.addTests(loader.loadTestsFromTestCase(DimensionConstruction))
suite.addTests(loader.loadTestsFromTestCase(DimensionAlgebra))
suite.addTests(loader.loadTestsFromTestCase(QualityScalingConstruction))

# === Extensions ===

# Deserialization
suite.addTests(loader.loadTestsFromTestCase(TestParseList))
suite.addTests(loader.loadTestsFromTestCase(TestDeserialize))

# Operators
suite.addTests(loader.loadTestsFromTestCase(TestOperators))

runner = unittest.TextTestRunner(verbosity=2)

if __name__ == "__main__":
    result = runner.run(suite)
