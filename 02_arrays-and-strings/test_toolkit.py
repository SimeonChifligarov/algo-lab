"""
Minimal tests for the arrays-and-strings toolkit.

How to run (from anywhere):
  python test_toolkit.py

or:
  python -m unittest 02_arrays-and-strings/test_toolkit.py

This file ensures the local folder is on sys.path so imports like `import array_ops`
work even when the working directory is the repo root.
"""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

# Ensure this directory (02_arrays-and-strings) is importable
THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from array_ops import reverse_in_place, rotate_left_in_place, rotate_right_in_place
from prefix_sums import PrefixSum, FenwickSum
from string_utils import (
    is_palindrome,
    are_anagrams,
    longest_common_prefix,
    reverse_words,
    run_length_encode,
    first_unique_char_index,
)


class TestArrayOps(unittest.TestCase):
    def test_reverse_in_place(self) -> None:
        a = [1, 2, 3]
        reverse_in_place(a)
        self.assertEqual(a, [3, 2, 1])

        b: list[int] = []
        reverse_in_place(b)
        self.assertEqual(b, [])

        c = [42]
        reverse_in_place(c)
        self.assertEqual(c, [42])

    def test_rotate_right_in_place(self) -> None:
        a = [1, 2, 3, 4, 5]
        rotate_right_in_place(a, 2)
        self.assertEqual(a, [4, 5, 1, 2, 3])

        b = [1, 2, 3, 4, 5]
        rotate_right_in_place(b, 0)
        self.assertEqual(b, [1, 2, 3, 4, 5])

        c = [1, 2, 3, 4, 5]
        rotate_right_in_place(c, 7)  # 7 % 5 = 2
        self.assertEqual(c, [4, 5, 1, 2, 3])

        d = [1, 2, 3, 4, 5]
        rotate_right_in_place(d, -1)  # right -1 == left 1
        self.assertEqual(d, [2, 3, 4, 5, 1])

    def test_rotate_left_in_place(self) -> None:
        a = [1, 2, 3, 4, 5]
        rotate_left_in_place(a, 2)
        self.assertEqual(a, [3, 4, 5, 1, 2])

        b = [1, 2, 3, 4, 5]
        rotate_left_in_place(b, -2)  # left -2 == right 2
        self.assertEqual(b, [4, 5, 1, 2, 3])


class TestPrefixSums(unittest.TestCase):
    def test_prefix_sum_basic(self) -> None:
        data = [3, -1, 4, 1, 5, 9]
        ps = PrefixSum.from_iterable(data)
        self.assertEqual(ps.n, 6)
        self.assertEqual(ps.total(), 21)
        self.assertEqual(ps.range_sum(0, 0), 0)
        self.assertEqual(ps.range_sum(0, 6), 21)
        self.assertEqual(ps.range_sum(1, 4), (-1) + 4 + 1)

    def test_prefix_sum_bounds(self) -> None:
        ps = PrefixSum.from_iterable([1, 2, 3])
        with self.assertRaises(IndexError):
            ps.range_sum(-1, 2)
        with self.assertRaises(IndexError):
            ps.range_sum(2, 1)
        with self.assertRaises(IndexError):
            ps.range_sum(0, 4)

    def test_fenwick_sum_basic_and_updates(self) -> None:
        data = [3, -1, 4, 1, 5, 9]
        fw = FenwickSum(data)
        self.assertEqual(fw.range_sum(0, 6), 21)
        self.assertEqual(fw.range_sum(1, 4), (-1) + 4 + 1)

        fw.add(2, 10)  # data[2] becomes 14
        self.assertEqual(fw.range_sum(0, 6), 31)
        self.assertEqual(fw.range_sum(2, 3), 14)

        fw.set(1, 7)  # data[1] becomes 7
        self.assertEqual(fw.range_sum(0, 2), 10)  # 3 + 7


class TestStringUtils(unittest.TestCase):
    def test_is_palindrome_default(self) -> None:
        self.assertTrue(is_palindrome("Racecar"))
        self.assertTrue(is_palindrome("A man, a plan, a canal: Panama"))
        self.assertFalse(is_palindrome("hello"))

    def test_is_palindrome_strict(self) -> None:
        # strict: case-sensitive, include punctuation
        self.assertFalse(is_palindrome("Racecar", case_insensitive=False))
        self.assertTrue(is_palindrome("a,a", alnum_only=False))  # punctuation included, still palindrome
        self.assertTrue(is_palindrome("a,a", alnum_only=True))  # punctuation ignored, "aa" palindrome

    def test_are_anagrams_default(self) -> None:
        self.assertTrue(are_anagrams("listen", "silent"))
        self.assertTrue(are_anagrams("Dormitory", "Dirty room!!"))
        self.assertFalse(are_anagrams("hello", "bello"))

    def test_longest_common_prefix(self) -> None:
        self.assertEqual(longest_common_prefix(["flower", "flow", "flight"]), "fl")
        self.assertEqual(longest_common_prefix(["dog", "racecar", "car"]), "")
        self.assertEqual(longest_common_prefix([]), "")
        self.assertEqual(longest_common_prefix(["", "abc"]), "")

    def test_reverse_words(self) -> None:
        self.assertEqual(reverse_words("  the   sky  is blue "), "blue is sky the")
        self.assertEqual(reverse_words("one two"), "two one")

    def test_run_length_encode(self) -> None:
        self.assertEqual(run_length_encode(""), "")
        self.assertEqual(run_length_encode("aaabbc"), "a3b2c")
        self.assertEqual(run_length_encode("abcd"), "abcd")
        self.assertEqual(run_length_encode("aaaaa"), "a5")

    def test_first_unique_char_index(self) -> None:
        self.assertEqual(first_unique_char_index("leetcode"), 0)
        self.assertEqual(first_unique_char_index("loveleetcode"), 2)
        self.assertEqual(first_unique_char_index("aabb"), -1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
