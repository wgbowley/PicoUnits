# pylint: skip-file
"""
Filename: operator.py

Descriptions:
    Tests the operator class and sub-methods 
    within the parser
"""

import unittest

from picounits.extensions.utilities.operations import Operations
from picounits.extensions.utilities.errors import UnknownOperator


class TestOperators(unittest.TestCase):
    """ Unit tests for the operator logic """
    def test_symbol(self):
        """ Test symbol direct lookup """
        items = [Operations.POWER, Operations.MULTIPLICATION, Operations.DIVIDED]
        expected = [['^'], ['*', 'x', '·', '∙'], ['/', '÷']]
        
        for index, item in enumerate(items):
            result = item.symbol
            self.assertEqual(result, expected[index])
    
    def test_repr_name(self):
        """ Test the operator object name is correct """
        items = [Operations.POWER, Operations.MULTIPLICATION, Operations.DIVIDED]
        types = [['^'], ['*', 'x', '·', '∙'], ['/', '÷']]
        
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
        test_items = ['^']
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
    
    def test_all_symbols_return(self):
        """ Test return method for all valid symbols """
        valid = ['*', 'x', '·', '∙', '/', '÷', '^',]
        
        result = Operations.all_symbols()
        self.assertEqual(result, valid)
    

if __name__ == '__main__':
    unittest.main()
