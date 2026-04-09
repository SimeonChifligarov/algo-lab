"""
Unit tests for randomized_quicksort.py
"""
import os
import sys

sys.path.append(os.path.dirname(__file__))

import unittest

from randomized_quicksort import randomized_quicksort, sorted_copy


class TestRandomizedQuicksort(unittest.TestCase):
    def test_empty_list(self) -> None:
        data = []
        randomized_quicksort(data)
        self.assertEqual(data, [])

    def test_single_element(self) -> None:
        data = [42]
        randomized_quicksort(data)
        self.assertEqual(data, [42])

    def test_basic_case(self) -> None:
        data = [9, 1, 7, 3, 8, 2, 6, 5, 4]
        randomized_quicksort(data)
        self.assertEqual(data, sorted([9, 1, 7, 3, 8, 2, 6, 5, 4]))

    def test_with_duplicates(self) -> None:
        data = [5, 1, 5, 3, 2, 3, 4, 5]
        randomized_quicksort(data)
        self.assertEqual(data, sorted([5, 1, 5, 3, 2, 3, 4, 5]))

    def test_negative_numbers(self) -> None:
        data = [-10, 7, 0, -3, 5, 2]
        randomized_quicksort(data)
        self.assertEqual(data, sorted([-10, 7, 0, -3, 5, 2]))

    def test_already_sorted(self) -> None:
        data = [1, 2, 3, 4, 5]
        randomized_quicksort(data)
        self.assertEqual(data, [1, 2, 3, 4, 5])

    def test_reverse_sorted(self) -> None:
        data = [5, 4, 3, 2, 1]
        randomized_quicksort(data)
        self.assertEqual(data, [1, 2, 3, 4, 5])

    def test_sorted_copy_returns_new_sorted_list(self) -> None:
        data = [9, 1, 7, 3, 8, 2, 6, 5, 4]
        original = list(data)

        result = sorted_copy(data)

        self.assertEqual(result, sorted(data))
        self.assertEqual(data, original)
        self.assertIsNot(result, data)

    def test_in_place_sort_modifies_list_correctly(self) -> None:
        data = [3, 1, 2]
        randomized_quicksort(data)
        self.assertEqual(data, [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
