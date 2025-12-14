"""
File: runner.py
Author: William Bowley
Version: 1.4

Description:
    Runs all unit tests within the pyFea framework
"""

import unittest

from tests.domain.unit_tests import UnitTest

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromTestCase(UnitTest))


runner = unittest.TextTestRunner(verbosity=2)

if __name__ == "__main__":
    result = runner.run(suite)