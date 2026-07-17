# pylint: skip-file
"""
Filename: syntax.py

Descriptions:
    Tests the syntax classes within the parser
    NOTE:   Classes | TestExtractionState, TestExtractPairs, 
            TestExtractBrackets, TestExtractParentheses
"""

import unittest

from picounits.extensions.utilities.errors import UnbalancedDepth
from picounits.extensions.core.syntax import (
    ExtractionState, ExtractPairs, ExtractBrackets, ExtractParentheses
)


class TestExtractionState(unittest.TestCase):
    """ Unit tests for testing extraction state functions """
    def test_distinguished_character(self):
        """ Initial quotes should toggle quote_char state """
        state = ExtractionState()
        state.quote_char = None
        state.index = 0
        line = '"hello'

        for characters in line:
            state.distinguished_character(characters)
            self.assertEqual(state.quote_char, '"')
    
    def test_distinguished_character_full_toggle(self):
        """ test quoted string ability to toggle quote_char on quoted line """
        state = ExtractionState()
        state.quote_char = None
        state.index = 0
        line = '"I am a quoted character"'
        
        for character in line:
            state.distinguished_character(character)
            
        self.assertIsNone(state.quote_char)

    def test_is_escaped_character_with_escaped(self):
        """ Tests extraction state with valid escaped character """
        state = ExtractionState()
        state.quote_char = None
        state.index = 0
        
        # Python encodes "\" as "\\" in source code
        line = '"1, 2, 3' + '\\',   # → "1, 2, 3\
        
        for character in line:
            escaped_state = state.is_escaped(character)
            
            if escaped_state:
                self.assertTrue(escaped_state)


class TestExtractPairs(unittest.TestCase):
    """ Unit tests for extract quality_name: value_pairs """
    def test_valid_key_value_pairs(self):
        """ Test `extract_key_value` function ability to split line on opened colon """
        items = ["test_quantity: 10 prefix(unit)", "mass: 10 m(kg)", "current: 1+1j M(A)"]
        expected = [
            ("test_quantity", "10 prefix(unit)"), ("mass", "10 m(kg)"), ("current", "1+1j M(A)")
        ]
        
        for index, item in enumerate(items):
            # Matches result with expected result
            result = ExtractPairs.extract_key_value(item)
            self.assertEqual(result, expected[index])
    
    def test_non_key_value_pairs(self):
        """ Test `extract_key_value` function ability to return `none` on non-pairs """
        items = ["test_quantity  10 prefix(unit)", "mass  10 M(m)", "speed10m(ms^-1)"]
        
        for item in items:
            result = ExtractPairs.extract_key_value(item)
            self.assertIsNone(result)
    
    def test_key_value_pairs_with_escaped_character(self):
        """ Test escaped colon is ignored and returns None"""
        line = r"item\: value prefix(unit)"
        expected = None  
        
        result = ExtractPairs.extract_key_value(line)
        self.assertEqual(result, expected)


class TestExtractBrackets(unittest.TestCase):
    """ Unit tests for Extracting content between matching bracket """
    def test_extract_content_with_no_open_bracket(self):
        """ Tests no open bracket found within the line """
        items = ["],1,2,3,4", "1+1j, 10.12, 'string']", "], ], ], ], ]"]

        for item in items:
            result = ExtractBrackets.extract_content(item)
            self.assertIsNone(result)

    def test_extract_valid_bracket(self):
        """ Tests extract content with valid brackets """
        items = ["[hello.my.together]", "[hello[son]]", "hello [son] bye"]
        expected = [["hello.my.together", 18], ["hello[son]", 11], ["son", 10]]
        
        for index, item in enumerate(items):
            raw_content, raw_index = ExtractBrackets.extract_content(item)
            exp_content, exp_index = expected[index]
            
            # Checks that the content and the end_index is correct
            self.assertEqual(raw_content, exp_content)
            self.assertEqual(raw_index, exp_index)
    
    def test_extract_with_escaped_character(self):
        """ Test escaped colon is ignored and returns the correct content """
        line = r"[item\: value prefix(unit)]"
        exp_content, exp_index = r"item\: value prefix(unit)", 26
        raw_content, raw_index = ExtractBrackets.extract_content(line)
        
        # Checks that the content and the end_index is correct
        self.assertEqual(raw_content, exp_content)
        self.assertEqual(raw_index, exp_index)

    def test_extract_with_unbalanced_depth(self):
        """ Test extract content with unbalanced depth of brackets """
        items = ["[hello.I.m.unbalanced[]", "[[I may be unbalanced", "[the cries of the carrots[]"]

        for item in items:
            with self.assertRaises(UnbalancedDepth):
                _ = ExtractBrackets.extract_content(item)


class TestExtractParentheses(unittest.TestCase):
    """ Unit tests for Extracting content between matching parenthesizes """
    def test_skip_non_parentheses(self):
        """ Tests skip non parenthesized characters with a series of tests """
        items, excepted = ["(hello)", "test (test)", "test"], [0, 5, 4]
        
        for index, item in enumerate(items):
            position = ExtractParentheses._skip_non_parentheses(item, 0)
            self.assertEqual(position, excepted[index])

    def test_extract_parentheses_content(self):
        """ Tests extracting parenthesized content """
        items = ["(hello (hello))", "(hello) (hello) (hello)", "hello (hello)"]
        expected = [['hello (hello)'], ['hello', 'hello', 'hello'], ['hello']]
        
        for index, item in enumerate(items):
            result = ExtractParentheses.extract_content(item)
            self.assertEqual(result, expected[index])

    def test_extract_parentheses_content_with_escaped_character(self):
        """ Test escaped colon is ignored and returns the correct content """
        line = r"(item\: value prefix(unit))"
        exp_content = [r"item\: value prefix(unit)"]

        raw_content = ExtractParentheses.extract_content(line)
        self.assertEqual(raw_content, exp_content)


if __name__ == '__main__':
    unittest.main()