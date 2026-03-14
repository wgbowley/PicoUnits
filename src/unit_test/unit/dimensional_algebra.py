"""
Filename: dimensional_algebra.py
Author: William Bowley

Description:
    Tests for the fundamental unit 'FBASE' and dataclass 'Dimension'
    to ensure that the dimensional algebra is correct for the application.
"""

import unittest
from picounits.core.dimensions import Dimension, FBase


class algebra(unittest.TestCase):
    """ Tests dimensional algebra system"""
    def test_construct_dimensions(self):
        """ Construct a dimension with each known base unit """
        for base in FBase:
            _ = Dimension(base, 1)


if __name__ == '__main__':
    unittest.main()
