"""
Unit tests for algorithm_comparison.py
"""
import os
import sys

sys.path.append(os.path.dirname(__file__))

import unittest

from ..algorithm_comparison import (
    benchmark,
    binary_search,
    format_seconds,
    linear_search,
    set_lookup,
)


class TestAlgorithmComparison(unittest.TestCase):
    def test_linear_search_found(self) -> None:
        data = [1, 2, 3, 4, 5]
        self.assertTrue(linear_search(data, 4))

    def test_linear_search_not_found(self) -> None:
        data = [1, 2, 3, 4, 5]
        self.assertFalse(linear_search(data, 99))

    def test_binary_search_found(self) -> None:
        data = [1, 2, 3, 4, 5]
        self.assertTrue(binary_search(data, 3))

    def test_binary_search_not_found(self) -> None:
        data = [1, 2, 3, 4, 5]
        self.assertFalse(binary_search(data, 99))

    def test_set_lookup_found(self) -> None:
        data = {1, 2, 3, 4, 5}
        self.assertTrue(set_lookup(data, 5))

    def test_set_lookup_not_found(self) -> None:
        data = {1, 2, 3, 4, 5}
        self.assertFalse(set_lookup(data, 99))

    def test_benchmark_returns_expected_keys(self) -> None:
        result = benchmark(linear_search, [1, 2, 3], 3, repeats=3)

        self.assertIn("min", result)
        self.assertIn("max", result)
        self.assertIn("mean", result)
        self.assertIn("median", result)

    def test_benchmark_invalid_repeats_raises(self) -> None:
        with self.assertRaises(ValueError):
            benchmark(linear_search, [1, 2, 3], 3, repeats=0)

    def test_benchmark_values_are_non_negative(self) -> None:
        result = benchmark(binary_search, [1, 2, 3, 4, 5], 3, repeats=3)

        for value in result.values():
            self.assertGreaterEqual(value, 0.0)

    def test_format_seconds_returns_string(self) -> None:
        self.assertIsInstance(format_seconds(0.0001), str)


if __name__ == "__main__":
    unittest.main()
