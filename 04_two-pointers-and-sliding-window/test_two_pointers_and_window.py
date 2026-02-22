"""
Tests for Two Pointers & Sliding Window toolkit (Part 4/4)

Run:
  python test_two_pointers_and_window.py

or:
  python -m unittest test_two_pointers_and_window.py
"""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

# Ensure this directory (04_two-pointers-and-sliding-window) is importable
THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from two_pointers import (
    pair_sum_sorted,
    is_palindrome_two_pointers,
    remove_duplicates_sorted,
    remove_element,
    move_zeros,
    remove_element_stable,
)

from sliding_window import (
    max_sum_subarray_k,
    average_subarray_k,
    min_subarray_len_at_least,
    longest_substring_k_distinct,
    longest_ones_after_replacement,
)

from patterns import (
    reverse_vowels,
    squares_sorted,
    container_with_most_water,
    is_subsequence,
    longest_substring_without_repeating,
    min_window_substring,
)


class TestTwoPointers(unittest.TestCase):
    def test_pair_sum_sorted(self) -> None:
        self.assertEqual(pair_sum_sorted([1, 2, 3, 4, 6], 6), (1, 3))
        self.assertEqual(pair_sum_sorted([1, 2, 3, 4, 6], 20), None)
        self.assertEqual(pair_sum_sorted([], 0), None)
        self.assertEqual(pair_sum_sorted([5], 5), None)

    def test_is_palindrome_two_pointers(self) -> None:
        self.assertTrue(is_palindrome_two_pointers("racecar"))
        self.assertFalse(is_palindrome_two_pointers("Racecar"))
        self.assertTrue(is_palindrome_two_pointers(""))
        self.assertTrue(is_palindrome_two_pointers("a"))
        self.assertFalse(is_palindrome_two_pointers("ab"))

    def test_remove_duplicates_sorted(self) -> None:
        a = [1, 1, 2, 2, 3]
        k = remove_duplicates_sorted(a)
        self.assertEqual(k, 3)
        self.assertEqual(a[:k], [1, 2, 3])

        b: list[int] = []
        self.assertEqual(remove_duplicates_sorted(b), 0)

        c = [1, 2, 3]
        k2 = remove_duplicates_sorted(c)
        self.assertEqual(k2, 3)
        self.assertEqual(c[:k2], [1, 2, 3])

    def test_remove_element_unstable(self) -> None:
        a = [3, 2, 2, 3]
        k = remove_element(a, 3)
        self.assertEqual(k, 2)
        self.assertEqual(sorted(a[:k]), [2, 2])

        b = [1, 2, 3]
        k2 = remove_element(b, 4)
        self.assertEqual(k2, 3)
        self.assertEqual(sorted(b[:k2]), [1, 2, 3])

    def test_move_zeros(self) -> None:
        a = [0, 1, 0, 3, 12]
        move_zeros(a)
        self.assertEqual(a, [1, 3, 12, 0, 0])

        b = [0, 0, 0]
        move_zeros(b)
        self.assertEqual(b, [0, 0, 0])

        c = [1, 2, 3]
        move_zeros(c)
        self.assertEqual(c, [1, 2, 3])

    def test_remove_element_stable(self) -> None:
        a = [3, 2, 2, 3]
        k = remove_element_stable(a, 3)
        self.assertEqual(k, 2)
        self.assertEqual(a[:k], [2, 2])


class TestSlidingWindow(unittest.TestCase):
    def test_max_sum_subarray_k(self) -> None:
        self.assertEqual(max_sum_subarray_k([2, 1, 5, 1, 3, 2], 3), 9)
        self.assertEqual(max_sum_subarray_k([1, 2, 3], 1), 3)
        with self.assertRaises(ValueError):
            max_sum_subarray_k([1, 2, 3], 0)
        with self.assertRaises(ValueError):
            max_sum_subarray_k([1, 2, 3], 4)

    def test_average_subarray_k(self) -> None:
        self.assertAlmostEqual(average_subarray_k([2, 1, 5, 1, 3, 2], 3), 3.0)

    def test_min_subarray_len_at_least(self) -> None:
        self.assertEqual(min_subarray_len_at_least([2, 3, 1, 2, 4, 3], 7), 2)
        self.assertEqual(min_subarray_len_at_least([1, 1, 1], 10), 0)
        self.assertEqual(min_subarray_len_at_least([], 7), 0)
        self.assertEqual(min_subarray_len_at_least([7], 7), 1)

    def test_longest_substring_k_distinct(self) -> None:
        self.assertEqual(longest_substring_k_distinct("eceba", 2), 3)  # "ece"
        self.assertEqual(longest_substring_k_distinct("aa", 1), 2)
        self.assertEqual(longest_substring_k_distinct("aa", 0), 0)

    def test_longest_ones_after_replacement(self) -> None:
        self.assertEqual(longest_ones_after_replacement([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2), 6)
        self.assertEqual(longest_ones_after_replacement([1, 1, 1], 0), 3)
        self.assertEqual(longest_ones_after_replacement([0, 0, 0], 1), 1)
        with self.assertRaises(ValueError):
            longest_ones_after_replacement([1, 0], -1)


class TestPatterns(unittest.TestCase):
    def test_reverse_vowels(self) -> None:
        self.assertEqual(reverse_vowels("hello"), "holle")
        self.assertEqual(reverse_vowels("aA"), "Aa")
        self.assertEqual(reverse_vowels("bcdf"), "bcdf")

    def test_squares_sorted(self) -> None:
        self.assertEqual(squares_sorted([-4, -1, 0, 3, 10]), [0, 1, 9, 16, 100])
        self.assertEqual(squares_sorted([]), [])
        self.assertEqual(squares_sorted([0]), [0])

    def test_container_with_most_water(self) -> None:
        self.assertEqual(container_with_most_water([1, 8, 6, 2, 5, 4, 8, 3, 7]), 49)
        self.assertEqual(container_with_most_water([1, 1]), 1)

    def test_is_subsequence(self) -> None:
        self.assertTrue(is_subsequence("abc", "ahbgdc"))
        self.assertFalse(is_subsequence("axc", "ahbgdc"))
        self.assertTrue(is_subsequence("", "ahbgdc"))

    def test_longest_substring_without_repeating(self) -> None:
        self.assertEqual(longest_substring_without_repeating("abcabcbb"), 3)
        self.assertEqual(longest_substring_without_repeating("bbbbb"), 1)
        self.assertEqual(longest_substring_without_repeating(""), 0)

    def test_min_window_substring(self) -> None:
        self.assertEqual(min_window_substring("ADOBECODEBANC", "ABC"), "BANC")
        self.assertEqual(min_window_substring("a", "a"), "a")
        self.assertEqual(min_window_substring("a", "aa"), "")
        self.assertEqual(min_window_substring("anything", ""), "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
