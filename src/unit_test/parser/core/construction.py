# pylint: skip-file
"""
Filename: construction.py

Descriptions:
    Tests the construction classes within the parser
    NOTE: Classes | TestConstructPrefix, TestConstructUnits, TestConstructQuality
"""

import unittest

from picounits.core.scales import _SYMBOLS_TO_SCALE
from picounits.core.unit import Unit
from picounits.constants import (
    TIME, LENGTH, MASS, CURRENT, TEMPERATURE, AMOUNT, LUMINOSITY, NULLSET,
    FORCE, PRESSURE, POWER
)

from picounits.extensions.core.construction import (
    ConstructPrefix, ConstructUnits, ConstructQuantity
)
from picounits.extensions.utilities.errors import (
    ParserError, UnknownPrefix, UnsupportedType
)


class TestConstructPrefix(unittest.TestCase):
    """ Unit tests for construct prefix class """
    def test_known_prefix(self):
        """ Construct prefix scale from text input """
        for symbol, scale in _SYMBOLS_TO_SCALE.items():
            result = ConstructPrefix.construct_prefix(symbol)
            self.assertEqual(result, scale)
    
    def test_unknown_prefix(self):
        """ Attempts to construct prefix scale from text input with unknown prefixes """
        symbols = ["hello", " k", "m ", "I'm in danger", "Au revoir"]
        
        for symbol in symbols:
            with self.assertRaises(UnknownPrefix):
                ConstructPrefix.construct_prefix(symbol) 
        

class TestConstructUnits(unittest.TestCase):
    """ Unit tests for construct units class """
    def test_unsupported_type(self):
        """ Attempts to parse unsupported types into the construct method """
        items = [1+2j, False, 1.10, 120, 10/21]
        
        for item in items:
            with self.assertRaises(UnsupportedType):
                ConstructUnits.construct_unit(item) 
        
    def test_handle_for_dimensionless(self):
        """ Passes empty string into the construct method """
        item = ""
        
        result = ConstructUnits.construct_unit(item)
        expected = Unit.dimensionless()
        self.assertEqual(result, expected)

    def test_tokenize_unit(self):
        """ Tests the unit string tokenizer """
        items = ["kg*m^2*s^-3*A^-1", "kg^-1*m^-2*s^4*A^2", "kg*m^2*s^-3*A^-2"]
        expected = [
            ['kg', '*', 'm', '^', '2', '*', 's', '^', '-3', '*', 'A', '^', '-1'],
            ['kg', '^', '-1', '*', 'm', '^', '-2', '*', 's', '^', '4', '*', 'A', '^', '2'],
            ['kg', '*', 'm', '^', '2', '*', 's', '^', '-3', '*', 'A', '^', '-2']
        ]
        
        for index, item in enumerate(items):
            result = ConstructUnits._tokenize_unit(item)
            self.assertEqual(result, expected[index])

    def test_no_tokens_return_path(self):
        """ Tests the return path if no tokens are returned by the tokenizer """
        items = [" ", "    ", ' ', '   ']
        
        for item in items:
            result = ConstructUnits.construct_unit(item)
            expected = Unit.dimensionless()
            self.assertEqual(result, expected)
    
    def test_single_dimensions_within_unit_string(self):
        """ Tests the single dimension within unit string return path """
        items = ["s", "m", "kg", "A", "K", "mol", "cd", "∅"]
        expected = [
            TIME, LENGTH, MASS, CURRENT, TEMPERATURE, AMOUNT, LUMINOSITY, NULLSET
        ]

        for index, item in enumerate(items):
            result = ConstructUnits.construct_unit(item)
            self.assertEqual(result, expected[index])
    
    def test_construct_unit_from_token_with_unknown_token(self):
        """ Tests the construct unit from token method with unknown token """
        items = [["{"], ['kg', '+', 'm'], ['mol', '@']]
        
        for item in items:
            with self.assertRaises(ParserError):
                ConstructUnits._construct_unit_from_tokens(item)
    
    def test_multi_dimensions_with_unit_string(self):
        """ Tests the multi dimensions within the unit string return path """
        items = ["kg*m*s^-2", "kg*m^-1*s^-2", "kg*m^2*s^-3", "kg/m"]
        expected = [FORCE, PRESSURE, POWER, MASS/LENGTH]
        
        for index, item in enumerate(items):
            result = ConstructUnits.construct_unit(item)
            self.assertEqual(result, expected[index])


# class TestConstructQuality(unittest.TestCase):
#     """ Unit tests for construct qualities class """
#     def test_column_prefix(self):
#         """ Tests the column prefix method with valid inputs """
#         item = [["k", "m", "M"], 2]
        
        

if __name__ == '__main__':
    unittest.main()
