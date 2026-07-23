# pylint: skip-file
"""
Filename: construction.py

Descriptions:
    Tests the construction classes within the parser
    NOTE: Classes | TestConstructPrefix, TestConstructUnits, TestConstructQuality
"""

import unittest

from picounits.core.scales import PrefixScale, _SYMBOLS_TO_SCALE
from picounits.core.unit import Unit
from picounits.core.quantities.packet import Packet

from picounits.constants import (
    TIME, LENGTH, MASS, CURRENT, TEMPERATURE, AMOUNT, LUMINOSITY, NULLSET,
    FORCE, PRESSURE, POWER, MILLI, KILO, MEGA
)

from picounits.extensions.core.construction import (
    ConstructPrefix, ConstructUnits, ConstructQuantity
)
from picounits.extensions.utilities.errors import (
    ParserError, UnknownPrefix, UnsupportedType, ColumnAttribute
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
        symbols = ["hello", "I'm in danger", "Au revoir"]
        
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
        items = ["kg*m*s^-2", "kg*m^-1*s^-2", "kg*m^2*s^-3", "kg/m^-1"]
        expected = [FORCE, PRESSURE, POWER, MASS*LENGTH]
        
        for index, item in enumerate(items):
            result = ConstructUnits.construct_unit(item)
            self.assertEqual(result, expected[index])
            
    def test_division_operations(self):
        """ Tests division operations in unit construction """
        items = ["kg/m", "m/s^2", "kg*m/s^2", "kg/m/s"]
        expected = [MASS / LENGTH, LENGTH / TIME**2, MASS * LENGTH / TIME**2, MASS / LENGTH / TIME]
        
        for index, item in enumerate(items):
            result = ConstructUnits.construct_unit(item)
            self.assertEqual(result, expected[index])

class TestConstructQuality(unittest.TestCase):
    """ Unit tests for construct qualities class """
    def test_non_numerical_value_input(self):
        """ Test return path for strings and booleans """
        items = [False, True, "Hello", "Tschuss", ""]
        
        for item in items:
            # Should pass the item back to the user.
            result = ConstructQuantity.quantity(item, None, None)
            self.assertEqual(result, item)
    
    def test_valid_single_qualities(self):
        """ Tests valid single qualities inputs for construction"""
        items = [[10, "m", "kg/mol"], [1+1j, "k", "m"], [10.10, "", "mol"]]
        expected = [10 * MILLI * MASS / AMOUNT, (1+1j) * KILO * LENGTH, 10.10 * AMOUNT]

        for index, item in enumerate(items):
            value, prefix, unit = item
            result = ConstructQuantity.quantity(value, prefix, unit)
            self.assertEqual(result, expected[index])

    def test_valid_array_qualities(self):
        """ Tests valid array qualities inputs for construction """
        items = [
            [[10,20,30,40], "m", "m/kg"], 
            [[1,2,3,4], "k", "m"], [[1.2, 1.3, 1.4], "", "mol"]
        ]
        expected: list[Packet] = [
            [10,20,30,40] * MILLI * LENGTH / MASS, 
            [1,2,3,4] * KILO * LENGTH, [1.2, 1.3, 1.4] * AMOUNT
        ]
    
        for index, item in enumerate(items):
            value, prefix, unit = item
            result = ConstructQuantity.quantity(value, prefix, unit)
            
            # Compares the result unit, expected unit and then the expected item within the array
            self.assertEqual(result.unit, expected[index].unit)
            self.assertEqual(result.stripped.tolist(), expected[index].stripped.tolist())
    
    def test_valid_nested_array_qualities(self):
        """ Test valid nested array qualities inputs for construction """
        value = [[1,2,3], [1,2,3], [1,2,3]]
        prefix = ["m", "k", "M"]
        units = ["kg", "m/mol", "A^-1"]
        
        expected_rows = [1 * MILLI * MASS, 2 * KILO * LENGTH / AMOUNT, 3 * MEGA * CURRENT ** -1]
        expected = [expected_rows, expected_rows, expected_rows]
        
        result = ConstructQuantity.quantity(value, prefix, units)
        self.assertEqual(result, expected)    
    
    def test_valid_nested_array_qualities_with_no_prefix(self):
        """ Test valid nested array qualities input for construction without prefix """
        value = [[1,2,3], [1,2,3], [1,2,3]]
        units = ["kg", "m/mol", "A^-1"]
        
        expected_rows = [1  * MASS, 2 * LENGTH / AMOUNT, 3 * CURRENT ** -1]
        expected = [expected_rows, expected_rows, expected_rows]
        
        result = ConstructQuantity.quantity(value, "", units)
        self.assertEqual(result, expected)    
    
    
    def test_column_prefix_with_valid_input(self):
        """ Tests the column prefix with valid input """
        items = [
            [[PrefixScale.MICRO, PrefixScale.MILLI, PrefixScale.MEGA], 2],
            [[PrefixScale.MICRO, PrefixScale.MEGA], 1], [[PrefixScale.BASE], 0]
        ]
    
        for item in items:
            prefix, index = item[0], item[1]
            result = ConstructQuantity._column_prefix(prefix, index)
            self.assertEqual(result, prefix[index])
    
    def test_column_Prefix_with_invalid_input(self):
        """ Tests the column prefix with invalid inputs for `ColumnAttribute` error """
        items = [
            [[PrefixScale.MICRO, PrefixScale.MILLI, PrefixScale.MEGA], 4],
            [[PrefixScale.MICRO, PrefixScale.MEGA], -1], [[PrefixScale.BASE], 100]
        ]
    
        for item in items:
            prefix, index = item[0], item[1]
            with self.assertRaises(ColumnAttribute):
                ConstructQuantity._column_prefix(prefix, index)
    
    def test_column_unit_with_valid_input(self):
        """ Tests the column unit with valid inputs """
        items = [[[TIME, LENGTH, AMOUNT], 1], [[LENGTH, CURRENT], 0], [[LENGTH], 0]]
        
        for item in items:
            units, index = item[0], item[1]
            result = ConstructQuantity._column_unit(units, index)
            self.assertEqual(result, units[index])

    def test_column_unit_with_invalid_inputs(self):
        """ Tests the column unit with invalid inputs for `ColumnAttribute` error """
        items = [[[TIME, MASS], 3], [[LENGTH, CURRENT, TIME], -10], [[LENGTH, CURRENT], -1]]
        
        for item in items:
            units, index = item[0], item[1]
            with self.assertRaises(ColumnAttribute):
                ConstructQuantity._column_unit(units, index)
            

if __name__ == '__main__':
    unittest.main()
