# pylint: skip-file
"""
Filename: core.py

Descriptions:
    Tests the core classes within the dsl_parser
"""

import unittest

from picounits.extensions.core.deserialization import Deserialize, ParseListStructure
from picounits.extensions.utilities.errors import ParseListFailure


class TestDeserialize(unittest.TestCase):
    """ Unit tests for Deserialize logic """
    def test_is_quoted(self):
        """ Tests is quoted function with strings. """
        items = ['"Hello"', '"171"', "'Hello'", "'1+2j'"]
        
        for item in items:
            result = Deserialize.is_quoted(item)
            self.assertEqual(result, True)

    def test_stripped(self):
        """ Tests to strip quotes from a series of strings """
        items = ['"Hello"', '"171"', "'Hello'", "'1+2j'"]
        stripped = ["Hello", "171", "Hello", "1+2j"]

        for index in range(0, len(items)):
            result = Deserialize.strip_quotes(items[index])
            self.assertEqual(result, stripped[index])

    def test_casting_complex(self):
        """ Tests casting a complex number from text to type """
        text = "1+2j"
        
        result = Deserialize.cast(text)
        self.assertIsInstance(result, complex)

    def test_casting_integer(self):
        """ Tests casting a integer value from text to type """
        text = "420"
        
        result = Deserialize.cast(text)
        self.assertIsInstance(result, int)

    def test_casting_float(self):
        """ Tests casting a float value from text to type """
        text = "420.232"
        
        result = Deserialize.cast(text)
        self.assertIsInstance(result, float)
        
    def test_boolean(self):
        """ Tests casting a boolean value from text to type """
        items = ["False", "True", "FaLse", "tRUE", "TRUE", "FALSE"]
        
        for item in items:
            result = Deserialize.cast(item)
            self.assertIsInstance(result, bool)

    def test_none_null(self):
        """ Tests casting a null/none value from text to type """
        items = ["null", "none", "NULL", "NONE", "nOnE", "Null"]

        for item in items:
            result = Deserialize.cast(item)
            self.assertIsNone(result)
            
    def test_string(self):
        """ Test casting a string from text to type """
        items = ["Hello", "Ich bin William", "Sohn", "Value is 121", "Ich bin 19"]

        for item in items:
            result = Deserialize.cast(item)
            self.assertIsInstance(result, str)
        
    def test_parse_list(self):
        """ Test casting a list from text to list structure """
        items = ["[1,2,3,4]", "[1,2,3,[1,2,3]]", "[1,[2,3,5]]"]
        
        for item in items:
            result = Deserialize.case_list(item)
            self.assertIsInstance(result, list)
        
    
class TestParseList(unittest.TestCase):
    """ Unit tests for ParseListStructure sectioning logic. """
    def test_invalid_test(self):
        """ Ensure the list is bounded """
        content = "[1,2,3,4], 5"

        with self.assertRaises(ParseListFailure):
            ParseListStructure.valid_list(content)

    def test_valid_test(self):
        """ Ensures the `valid_list` can detect bounded list"""
        content = "[1,2,3,4,5]"

        result = ParseListStructure.valid_list(content)
        self.assertEqual(result, None)

    def test_skip_whitespaces_with_whitespaces(self):
        """ Ensures the skip whitespace function acts correctly """
        content = "        100, 12, 21"

        result = ParseListStructure._skip_whitespaces(content, 0, len(content))
        self.assertEqual(result, 8)
        
    def test_skip_whitespaces_with_zero_whitespaces(self):
        """ Ensures the skip whitespace function returns zero when there are no whitespaces """
        content = "100, 12, 21"

        result = ParseListStructure._skip_whitespaces(content, 0, len(content))
        self.assertEqual(result, 0)
        
    def test_nested_brackets(self):
        """ Ensure list tokenizer ignores commas inside nested brackets. """
        content = "[1, 2], 3"
        index = ParseListStructure.tokenizer(content, 0, len(content))
        self.assertEqual(index, 6)

    def test_escaped_quotes(self):
        """ Ensure list tokenizer treats quoted commas as literal content. """
        content = "\"a, b\", 3"
        index = ParseListStructure.tokenizer(content, 0, len(content))
        self.assertEqual(index, 6)


if __name__ == '__main__':
    unittest.main()
