import os
import sys

sys.path.append(os.path.dirname(__file__))

import unittest

from bit_applications import (
    BitFlags,
    find_missing_number,
    find_single_number,
    find_subset_sum,
    find_two_single_numbers,
    max_xor_pair,
    min_assignment_cost,
    subset_sum_exists,
    xor_swap,
)


class TestBitApplications(unittest.TestCase):
    def test_xor_swap(self):
        self.assertEqual(xor_swap(5, 9), (9, 5))
        self.assertEqual(xor_swap(0, 7), (7, 0))
        self.assertEqual(xor_swap(-3, 4), (4, -3))

    def test_find_single_number(self):
        self.assertEqual(find_single_number([2, 1, 2]), 1)
        self.assertEqual(find_single_number([4, 1, 2, 1, 2]), 4)
        self.assertEqual(find_single_number([99]), 99)

    def test_find_two_single_numbers(self):
        self.assertEqual(find_two_single_numbers([1, 2, 1, 3, 2, 5]), (3, 5))
        self.assertEqual(find_two_single_numbers([4, 1, 2, 1, 2, 7]), (4, 7))

    def test_find_missing_number(self):
        self.assertEqual(find_missing_number([0, 1, 3], 3), 2)
        self.assertEqual(find_missing_number([1, 2, 3, 4], 4), 0)
        self.assertEqual(find_missing_number([0], 1), 1)

    def test_subset_sum_exists(self):
        self.assertTrue(subset_sum_exists([3, 5, 7, 9], 12))
        self.assertTrue(subset_sum_exists([1, 2, 3], 0))
        self.assertFalse(subset_sum_exists([4, 6, 8], 5))

    def test_find_subset_sum(self):
        self.assertEqual(sum(find_subset_sum([3, 5, 7, 9], 12)), 12)
        self.assertEqual(find_subset_sum([1, 2, 3], 0), [])
        self.assertEqual(find_subset_sum([4, 6, 8], 5), [])

    def test_min_assignment_cost(self):
        cost = [
            [9, 2, 7],
            [6, 4, 3],
            [5, 8, 1],
        ]
        self.assertEqual(min_assignment_cost(cost), 9)

    def test_min_assignment_cost_empty(self):
        self.assertEqual(min_assignment_cost([]), 0)

    def test_min_assignment_cost_invalid(self):
        with self.assertRaises(ValueError):
            min_assignment_cost([[1, 2], [3]])

    def test_max_xor_pair(self):
        self.assertEqual(max_xor_pair([3, 10, 5, 25, 2, 8]), 28)
        self.assertEqual(max_xor_pair([0, 2]), 2)
        self.assertEqual(max_xor_pair([7]), 0)
        self.assertEqual(max_xor_pair([]), 0)

    def test_bitflags_basic(self):
        flags = BitFlags()
        self.assertEqual(flags.value(), 0)
        self.assertEqual(flags.enabled_positions(), [])

        flags.enable(1)
        flags.enable(4)
        self.assertTrue(flags.is_enabled(1))
        self.assertTrue(flags.is_enabled(4))
        self.assertFalse(flags.is_enabled(3))

        flags.toggle(2)
        self.assertTrue(flags.is_enabled(2))

        flags.disable(1)
        self.assertFalse(flags.is_enabled(1))

        self.assertEqual(flags.enabled_positions(), [2, 4])

    def test_bitflags_reset(self):
        flags = BitFlags()
        flags.enable(0)
        flags.enable(3)
        flags.reset()
        self.assertEqual(flags.value(), 0)
        self.assertEqual(flags.enabled_positions(), [])

    def test_bitflags_invalid_position(self):
        flags = BitFlags()
        with self.assertRaises(ValueError):
            flags.enable(-1)
        with self.assertRaises(ValueError):
            flags.disable(-1)
        with self.assertRaises(ValueError):
            flags.toggle(-1)
        with self.assertRaises(ValueError):
            flags.is_enabled(-1)


if __name__ == "__main__":
    unittest.main()
