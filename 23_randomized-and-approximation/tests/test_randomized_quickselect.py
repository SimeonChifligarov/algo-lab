"""
Unit tests for randomized_quickselect.py
"""
import os
import sys

sys.path.append(os.path.dirname(__file__))

import unittest

from ..randomized_quickselect import kth_smallest, randomized_quickselect


class TestRandomizedQuickselect(unittest.TestCase):
    def test_basic_case(self) -> None:
        data = [7, 2, 1, 8, 6, 3, 5, 4]
        for k in range(len(data)):
            self.assertEqual(kth_smallest(data, k), sorted(data)[k])

    def test_with_duplicates(self) -> None:
        data = [5, 1, 5, 3, 2, 3, 4]
        for k in range(len(data)):
            self.assertEqual(kth_smallest(data, k), sorted(data)[k])

    def test_single_element(self) -> None:
        self.assertEqual(kth_smallest([42], 0), 42)

    def test_negative_numbers(self) -> None:
        data = [-10, 7, 0, -3, 5, 2]
        for k in range(len(data)):
            self.assertEqual(kth_smallest(data, k), sorted(data)[k])

    def test_empty_input_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            kth_smallest([], 0)

    def test_k_too_small_raises_index_error(self) -> None:
        with self.assertRaises(IndexError):
            kth_smallest([1, 2, 3], -1)

    def test_k_too_large_raises_index_error(self) -> None:
        with self.assertRaises(IndexError):
            kth_smallest([1, 2, 3], 3)

    def test_safe_wrapper_does_not_modify_original_list(self) -> None:
        data = [9, 1, 7, 3, 8, 2, 6, 5, 4]
        original = list(data)

        result = kth_smallest(data, 4)

        self.assertEqual(result, 5)
        self.assertEqual(data, original)

    def test_in_place_version_returns_correct_result(self) -> None:
        data = [9, 1, 7, 3, 8, 2, 6, 5, 4]
        result = randomized_quickselect(data, 4)
        self.assertEqual(result, 5)


if __name__ == "__main__":
    unittest.main()
