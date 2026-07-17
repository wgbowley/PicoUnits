# pylint: skip-file
"""
Filename: deserialization.py

Descriptions:
    Tests the deserialization classes within the parser
    NOTE: Classes | TestDeserialize, TestParseList
"""

import unittest

from picounits.extensions.core.deserialization import Deserialize, ParseListStructure
from picounits.extensions.utilities.errors import ParseListFailure, FailedCasting


class TestDeserialize(unittest.TestCase):
    """ Unit tests for Deserialize logic """
    def test_is_quoted(self):
        """ Tests is_quoted function with quoted strings. """
        items = ['"Hello"', '"171"', "'Hello'", "'1+2j'"]
        
        for item in items:
            result = Deserialize.is_quoted(item)
            self.assertEqual(result, True)

    def test_is_not_quoted(self):
        """ Tests is_quoted function with unquoted strings"""
        items = ['Guten Tag', 'William', '10.21+10j', '1.021']

        for item in items:
            result = Deserialize.is_quoted(item)
            self.assertEqual(result, False)
    
    def test_stripped(self):
        """ Tests to strip quotes from a series of strings """
        items = ['"Hello"', '"171"', "'Hello'", "'1+2j'"]
        stripped = ["Hello", "171", "Hello", "1+2j"]

        for index in range(0, len(items)):
            result = Deserialize.strip_quotes(items[index])
            self.assertEqual(result, stripped[index])

    def test_strip_non_quoted(self):
        """ Tests to strip non-quoted strings """
        test = ["Hello", "171", "Hello", "1+2j"]
        
        for item in test:
            result = Deserialize.strip_quotes(item)
            self.assertEqual(result, item)

    def test_failed_casting_due_to_non_string(self):
        """ Tests casting with a non-string as input """
        items = [10, 10.12, False, [1,2,3,4], {"key":"value"}]
        
        for item in items:
            with self.assertRaises(FailedCasting):
                Deserialize.cast(item)

    def test_casting_quoted_string(self):
        """ Tests casting a quoted string from text to type """
        double_quotes = '"I am a double quoted string"'
        single_quotes = "'I am a single quoted string'"
        
        for item in (double_quotes, single_quotes):
            result = Deserialize.cast(item)
            expected = item[1:-1]
            self.assertEqual(result, expected)
    
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
    
    def test_parse_list_with_non_strings(self):
        """ Test casting a list from non-string types """
        items = [10, 10.12, False, [1,2,3,4], {"key":"value"}]
        
        for item in items:
            with self.assertRaises(FailedCasting):
                Deserialize.case_list(item)
    
class TestParseList(unittest.TestCase):
    """ Unit tests for ParseListStructure sectioning logic. """
    def test_valid_list(self):
        """ Ensures the `valid_list` can detect bounded list"""
        content = "[1,2,3,4,5]"

        result = ParseListStructure.valid_list(content)
        self.assertEqual(result, None)
    
    def test_invalid_list(self):
        """ Ensure the list is bounded """
        content = "[1,2,3,4], 5"

        with self.assertRaises(ParseListFailure):
            ParseListStructure.valid_list(content)

    def test_invalid_type_for_valid_list(self):
        """ Ensures the `valid_list` can detect invalid structures """
        items = ["Hello", "test", "incorrect", " ", "''"]
        
        for item in items:
            with self.assertRaises(ParseListFailure):
                ParseListStructure.valid_list(item)

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

    def test_empty_element_found(self):
        """ Ensures the construct_list function raises an error on empty elements """
        items = ["1,2,,3", "1,2,,", ",,", "1,2, "]
        
        for item in items:
            with self.assertRaises(ParseListFailure):
                ParseListStructure.construct_list(item)
            
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
    
    def test_tokenizer_with_unterminated_escape(self):
        """ Ensures unterminated escape raises error """
        items = [
            '"1, 2, 3' + '\\',   # → "1, 2, 3\
            '"1, 2' + '\\',      # → "1, 2\
            '"hello' + '\\',     # → "hello\
        ]

        for item in items:
            with self.assertRaises(ParseListFailure):
                ParseListStructure.construct_list(item)

    def test_tokenizer_with_unterminated_string(self):
        """ Ensures unterminated strings raise an error """
        items = ["'hello", "hello'", 'ich bin"', "'nein"]
        
        for item in items:
            with self.assertRaises(ParseListFailure):
                ParseListStructure.construct_list(item)
        
           
    def test_tokenizer_with_unbalanced_list(self):
        """ Test the tokenizer with a series of unbalanced list structure """
        items = ["1,2,[1,2,3", "[1,2,3", "'1','2','3',[", "1,2,3,]"]
        
        for item in items:
            with self.assertRaises(ParseListFailure):
                ParseListStructure.construct_list(item)
    
    def test_recursive_descent_with_malformed_list(self):
        """ Tests recursive descent with a malformed list """
        content = "[1,2,3,4], 5"

        with self.assertRaises(ParseListFailure):
            ParseListStructure._recursive_descent(content)


if __name__ == '__main__':
    unittest.main()
