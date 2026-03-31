import os
import sys

sys.path.append(os.path.dirname(__file__))

import unittest

from prefix_function import prefix_function, lps_array


class TestPrefixFunction(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(prefix_function(""), [])
        self.assertEqual(lps_array(""), [])

    def test_single_character(self):
        self.assertEqual(prefix_function("a"), [0])

    def test_all_same_characters(self):
        self.assertEqual(prefix_function("aaaa"), [0, 1, 2, 3])

    def test_mixed_pattern(self):
        self.assertEqual(prefix_function("ababaca"), [0, 0, 1, 2, 3, 0, 1])

    def test_no_repeated_prefix(self):
        self.assertEqual(prefix_function("abcd"), [0, 0, 0, 0])

    def test_partial_repetition(self):
        self.assertEqual(prefix_function("abcab"), [0, 0, 0, 1, 2])

    def test_lps_alias_matches_prefix_function(self):
        pattern = "ababcabab"
        self.assertEqual(lps_array(pattern), prefix_function(pattern))

    def test_longer_example(self):
        s = "aabaaab"
        self.assertEqual(prefix_function(s), [0, 1, 0, 1, 2, 2, 3])


if __name__ == "__main__":
    unittest.main()
