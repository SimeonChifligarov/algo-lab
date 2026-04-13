import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import unittest

from ..kmp_search import (
    build_lps,
    contains_pattern,
    count_occurrences,
    first_occurrence,
    kmp_search,
)


class TestKMPSearch(unittest.TestCase):
    def test_build_lps(self):
        self.assertEqual(build_lps("ababd"), [0, 0, 1, 2, 0])

    def test_empty_pattern(self):
        self.assertEqual(kmp_search("abc", ""), [0, 1, 2, 3])

    def test_pattern_longer_than_text(self):
        self.assertEqual(kmp_search("abc", "abcd"), [])

    def test_single_match(self):
        self.assertEqual(kmp_search("ababcabcabababd", "ababd"), [10])

    def test_multiple_matches(self):
        self.assertEqual(kmp_search("aaaaa", "aa"), [0, 1, 2, 3])

    def test_no_match(self):
        self.assertEqual(kmp_search("abcdef", "gh"), [])

    def test_full_text_match(self):
        self.assertEqual(kmp_search("pattern", "pattern"), [0])

    def test_contains_pattern_true(self):
        self.assertTrue(contains_pattern("abracadabra", "cada"))

    def test_contains_pattern_false(self):
        self.assertFalse(contains_pattern("abracadabra", "cadax"))

    def test_first_occurrence_found(self):
        self.assertEqual(first_occurrence("abracadabra", "abra"), 0)

    def test_first_occurrence_not_found(self):
        self.assertEqual(first_occurrence("abracadabra", "xyz"), -1)

    def test_first_occurrence_empty_pattern(self):
        self.assertEqual(first_occurrence("abc", ""), 0)

    def test_count_occurrences(self):
        self.assertEqual(count_occurrences("aaaaa", "aa"), 4)

    def test_overlapping_matches(self):
        self.assertEqual(kmp_search("abababa", "aba"), [0, 2, 4])


if __name__ == "__main__":
    unittest.main()
