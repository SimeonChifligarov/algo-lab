import os
import sys

sys.path.append(os.path.dirname(__file__))

import unittest

from house_robber_and_kadane import (
    house_robber,
    house_robber_with_table,
    kadane_max_subarray,
    kadane_with_indices,
)


class TestHouseRobber(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(house_robber([]), 0)
        self.assertEqual(house_robber_with_table([]), 0)

    def test_single_house(self):
        self.assertEqual(house_robber([5]), 5)
        self.assertEqual(house_robber_with_table([5]), 5)

    def test_two_houses(self):
        self.assertEqual(house_robber([2, 7]), 7)
        self.assertEqual(house_robber_with_table([2, 7]), 7)

    def test_known_example(self):
        nums = [2, 7, 9, 3, 1]

        self.assertEqual(house_robber(nums), 12)
        self.assertEqual(house_robber_with_table(nums), 12)

    def test_alternating_values(self):
        nums = [5, 1, 5, 1, 5]

        self.assertEqual(house_robber(nums), 15)
        self.assertEqual(house_robber_with_table(nums), 15)

    def test_all_equal(self):
        nums = [4, 4, 4, 4]

        self.assertEqual(house_robber(nums), 8)
        self.assertEqual(house_robber_with_table(nums), 8)

    def test_increasing_values(self):
        nums = [1, 2, 3, 4, 5]

        self.assertEqual(house_robber(nums), 9)
        self.assertEqual(house_robber_with_table(nums), 9)

    def test_decreasing_values(self):
        nums = [5, 4, 3, 2, 1]

        self.assertEqual(house_robber(nums), 9)
        self.assertEqual(house_robber_with_table(nums), 9)

    def test_all_implementations_match(self):
        test_cases = [
            [],
            [1],
            [1, 2],
            [2, 1, 1, 2],
            [10, 5, 15, 20, 2, 30],
        ]

        for nums in test_cases:
            with self.subTest(nums=nums):
                self.assertEqual(
                    house_robber(nums),
                    house_robber_with_table(nums),
                )


class TestKadane(unittest.TestCase):
    def test_single_element(self):
        nums = [5]

        self.assertEqual(kadane_max_subarray(nums), 5)
        self.assertEqual(kadane_with_indices(nums), (5, 0, 0))

    def test_all_positive(self):
        nums = [1, 2, 3, 4]

        self.assertEqual(kadane_max_subarray(nums), 10)
        self.assertEqual(kadane_with_indices(nums), (10, 0, 3))

    def test_all_negative(self):
        nums = [-5, -1, -8]

        self.assertEqual(kadane_max_subarray(nums), -1)
        self.assertEqual(kadane_with_indices(nums), (-1, 1, 1))

    def test_mixed_values_known_example(self):
        nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

        self.assertEqual(kadane_max_subarray(nums), 6)
        self.assertEqual(kadane_with_indices(nums), (6, 3, 6))

    def test_multiple_possible_subarrays(self):
        nums = [1, -1, 1, -1, 1]

        self.assertEqual(kadane_max_subarray(nums), 1)

        max_sum, start, end = kadane_with_indices(nums)
        self.assertEqual(max_sum, 1)
        self.assertTrue(0 <= start <= end < len(nums))

    def test_large_positive_segment(self):
        nums = [-10, -5, 2, 3, 4, -1, 2]

        self.assertEqual(kadane_max_subarray(nums), 10)
        self.assertEqual(kadane_with_indices(nums), (10, 2, 6))

    def test_empty_input_raises_value_error(self):
        with self.assertRaises(ValueError):
            kadane_max_subarray([])

        with self.assertRaises(ValueError):
            kadane_with_indices([])

    def test_indices_match_sum(self):
        nums = [3, -2, 5, -1]

        max_sum, start, end = kadane_with_indices(nums)

        self.assertEqual(max_sum, sum(nums[start:end + 1]))
        self.assertEqual(max_sum, kadane_max_subarray(nums))


if __name__ == "__main__":
    unittest.main()
