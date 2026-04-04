import os
import sys

sys.path.append(os.path.dirname(__file__))

import unittest

from rolling_hash import (
    RollingHash,
    contains_pattern_hash,
    count_occurrences_hash,
    find_duplicate_substrings,
    group_identical_substrings,
    longest_repeated_substring,
    rabin_karp_search,
)


class TestRollingHash(unittest.TestCase):
    def test_full_hash_matches_full_substring_hash(self):
        rh = RollingHash("banana")
        self.assertEqual(rh.full_hash(), rh.hash_substring(0, 6))

    def test_equal_substrings_same_hash(self):
        rh = RollingHash("banana")
        self.assertEqual(rh.hash_substring(1, 4), rh.hash_substring(3, 6))  # "ana"

    def test_compare_substrings_true(self):
        rh = RollingHash("banana")
        self.assertTrue(rh.compare_substrings(1, 4, 3, 6))

    def test_compare_substrings_false(self):
        rh = RollingHash("banana")
        self.assertFalse(rh.compare_substrings(0, 3, 1, 4))

    def test_invalid_substring_range_raises(self):
        rh = RollingHash("abc")
        with self.assertRaises(ValueError):
            rh.hash_substring(-1, 2)

        with self.assertRaises(ValueError):
            rh.hash_substring(2, 1)

        with self.assertRaises(ValueError):
            rh.hash_substring(0, 4)

    def test_longest_common_prefix(self):
        rh = RollingHash("banana")
        self.assertEqual(rh.longest_common_prefix(1, 3), 3)  # "ana"

    def test_rabin_karp_empty_pattern(self):
        self.assertEqual(rabin_karp_search("abc", ""), [0, 1, 2, 3])

    def test_rabin_karp_pattern_longer_than_text(self):
        self.assertEqual(rabin_karp_search("abc", "abcd"), [])

    def test_rabin_karp_single_match(self):
        self.assertEqual(rabin_karp_search("abracadabra", "cada"), [4])

    def test_rabin_karp_multiple_matches(self):
        self.assertEqual(rabin_karp_search("aaaaa", "aa"), [0, 1, 2, 3])

    def test_contains_pattern_hash(self):
        self.assertTrue(contains_pattern_hash("abracadabra", "abra"))
        self.assertFalse(contains_pattern_hash("abracadabra", "xyz"))

    def test_count_occurrences_hash(self):
        self.assertEqual(count_occurrences_hash("aaaaa", "aa"), 4)

    def test_find_duplicate_substrings(self):
        self.assertEqual(find_duplicate_substrings("banana", 2), ["an", "na"])
        self.assertEqual(find_duplicate_substrings("banana", 3), ["ana"])

    def test_find_duplicate_substrings_invalid_length(self):
        self.assertEqual(find_duplicate_substrings("banana", 0), [])
        self.assertEqual(find_duplicate_substrings("banana", 10), [])

    def test_longest_repeated_substring(self):
        self.assertEqual(longest_repeated_substring("banana"), "ana")
        self.assertEqual(longest_repeated_substring("abcd"), "")
        self.assertEqual(longest_repeated_substring(""), "")

    def test_group_identical_substrings(self):
        groups = group_identical_substrings("banana", 3)
        expected = [
            [(1, "ana"), (3, "ana")],
        ]
        self.assertEqual(groups, expected)


if __name__ == "__main__":
    unittest.main()
