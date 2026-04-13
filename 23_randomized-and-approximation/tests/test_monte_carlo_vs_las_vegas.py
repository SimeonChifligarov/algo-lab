"""
Unit tests for monte_carlo_vs_las_vegas.py
"""
import os
import sys

sys.path.append(os.path.dirname(__file__))

import unittest

from ..monte_carlo_vs_las_vegas import (
    estimate_pi,
    las_vegas_search,
)


class TestMonteCarlo(unittest.TestCase):
    def test_estimate_pi_reasonable_accuracy(self) -> None:
        """
        With enough samples, the estimate should be close to math.pi.
        We allow a small error margin since this is randomized.
        """
        estimate = estimate_pi(100_000)
        self.assertTrue(3.0 < estimate < 3.3)

    def test_estimate_pi_small_samples(self) -> None:
        """
        Even with small samples, result should be within a broad valid range.
        """
        estimate = estimate_pi(100)
        self.assertTrue(0.0 < estimate <= 4.0)

    def test_estimate_pi_invalid_input(self) -> None:
        with self.assertRaises(ValueError):
            estimate_pi(0)

        with self.assertRaises(ValueError):
            estimate_pi(-10)


class TestLasVegasSearch(unittest.TestCase):
    def test_find_existing_element(self) -> None:
        data = [10, 20, 30, 40, 50]
        target = 30

        result = las_vegas_search(data, target)

        self.assertIsNotNone(result)
        self.assertEqual(data[result], target)

    def test_find_with_duplicates(self) -> None:
        data = [1, 2, 3, 2, 4, 2]
        target = 2

        result = las_vegas_search(data, target)

        self.assertIsNotNone(result)
        self.assertEqual(data[result], target)

    def test_target_not_found(self) -> None:
        data = [1, 2, 3, 4, 5]
        target = 99

        result = las_vegas_search(data, target)

        self.assertIsNone(result)

    def test_empty_list(self) -> None:
        result = las_vegas_search([], 10)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
