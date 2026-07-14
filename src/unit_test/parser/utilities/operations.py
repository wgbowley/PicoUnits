# pylint: skip-file
"""
Filename: operator.py

Descriptions:
    Tests the operator class and sub-methods 
    within the parser
"""

import unittest

from picounits.extensions.utilities.operations import Operations
from picounits.extensions.utilities.errors import UnknownOperator, AmbiguousPower


class TestOperators(unittest.TestCase):
    """ Unit tests for the operator logic """
    def test_symbol(self):
        """ Test symbol direct lookup """
        items = [Operations.POWER, Operations.MULTIPLICATION, Operations.DIVIDED]
        expected = [
            ['^', '⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹'],
            ['*', 'x', '·', '∙'], 
            ['/', '÷'], 
        ]
        
        for index, item in enumerate(items):
            result = item.symbol
            self.assertEqual(result, expected[index])
    
    def test_repr_name(self):
        """ Test the operator object name is correct """
        items = [Operations.POWER, Operations.MULTIPLICATION, Operations.DIVIDED]
        types = [
            ['^', '⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹'],
            ['*', 'x', '·', '∙'], 
            ['/', '÷'], 
        ]
        
        for index, item in enumerate(items):
            result = item._repr_name
            expected = f"<Operations type={item.name}, symbol={types[index]}>"
            self.assertEqual(result, expected)
            
            # Ensure string representation is correct
            repr_result = item.__repr__()
            str_result = item.__str__()
            
            self.assertEqual(repr_result, expected)
            self.assertEqual(str_result, expected)
    
    def test_from_power_symbol(self):
        """ Test creation of power operator object via symbol lookup """
        test_items = ['^', '⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹']
        expected_operator = Operations.POWER

        for item in test_items:
            result_operator = Operations.from_symbol(item)
            self.assertEqual(result_operator, expected_operator)
    
    def test_from_multiplication_symbol(self):
        """ Test creation of multiplication operator object via symbol lookup """
        test_items = ['*', 'x', '·', '∙']
        expected_operator = Operations.MULTIPLICATION

        for item in test_items:
            result_operator = Operations.from_symbol(item)
            self.assertEqual(result_operator, expected_operator)
            
    def test_from_division_symbol(self):
        """ Test creation of division operator object via symbol lookup """
        test_items = ['/', '÷']
        expected_operator = Operations.DIVIDED

        for item in test_items:
            result_operator = Operations.from_symbol(item)
            self.assertEqual(result_operator, expected_operator)
            
    def test_from_unknown_symbol(self):
        """ Test attempted creation from unknown operator symbol """
        test_item = ['^^', '***', '///', '÷÷', 'xx', '··']
        
        for item in test_item:
            with self.assertRaises(UnknownOperator):
                 Operations.from_symbol(item)
    
    def test_validate_unicode_usage(self):
        """ Ensures non mixing of power symbol & unicode """
        items = [["^", "1", "0"], ["^", "-", "6"], ['^', '1'], ['¹'], ['²']]
        
        for item in items:
            result = Operations.validate_unicode_usage(item)
            self.assertIsNone(result)
    
    def test_invalidate_unicode_usage(self):
        """ Ensures invalidate usage of unicode and power symbol raises error """
        items = [["^", '⁰', '¹'], ["^", "1", "⁰"], ["^", "¹"]]

        for item in items:
            with self.assertRaises(AmbiguousPower):
                Operations.validate_unicode_usage(item)
    
    def test_check_unicode_power(self):
        """ Test conversion system for unicode powers to integers """
        items = ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹']
        expected = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        for index, item in enumerate(items):
            result = Operations.check_unicode_power(item)
            self.assertEqual(result, expected[index])
    
    def test_non_unicode_types(self):
        """ Test non unicode types """
        items = ["1", "2", "1+2j", "software", "Maxwell is my sprit animal"]
        
        for item in items:
            result = Operations.check_unicode_power(item)
            self.assertEqual(result, False)
    
    def test_all_symbols_return(self):
        """ Test return method for all valid symbols """
        valid = [
            '*', 'x', '·', '∙', '/', '÷', '^', '⁰', '¹', 
            '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹'
        ]
        
        result = Operations.all_symbols()
        self.assertEqual(result, valid)
    

if __name__ == '__main__':
    unittest.main()
