"""
Unit tests for input_scaling_benchmark.py
"""
import os
import sys

sys.path.append(os.path.dirname(__file__))

import unittest

from ..input_scaling_benchmark import (
    benchmark,
    binary_search,
    format_seconds,
    linear_search,
    run_scaling_benchmark,
)


class TestInputScalingBenchmark(unittest.TestCase):
    def test_linear_search_found(self) -> None:
        data = [10, 20, 30, 40]
        self.assertEqual(linear_search(data, 30), 2)

    def test_linear_search_not_found(self) -> None:
        data = [10, 20, 30, 40]
        self.assertEqual(linear_search(data, 99), -1)

    def test_binary_search_found(self) -> None:
        data = [10, 20, 30, 40, 50]
        self.assertEqual(binary_search(data, 40), 3)

    def test_binary_search_not_found(self) -> None:
        data = [10, 20, 30, 40, 50]
        self.assertEqual(binary_search(data, 99), -1)

    def test_binary_search_empty(self) -> None:
        self.assertEqual(binary_search([], 5), -1)

    def test_benchmark_invalid_repeats_raises(self) -> None:
        with self.assertRaises(ValueError):
            benchmark(linear_search, [1, 2, 3], 2, repeats=0)

    def test_run_scaling_benchmark_returns_one_row_per_size(self) -> None:
        sizes = [10, 20, 30]

        def build_input(size: int) -> tuple[list[int], int]:
            return list(range(size)), size - 1

        results = run_scaling_benchmark(
            linear_search,
            sizes,
            build_input,
            repeats=2,
        )

        self.assertEqual(len(results), len(sizes))

    def test_run_scaling_benchmark_row_structure(self) -> None:
        sizes = [10]

        def build_input(size: int) -> tuple[list[int], int]:
            return list(range(size)), size - 1

        results = run_scaling_benchmark(
            linear_search,
            sizes,
            build_input,
            repeats=2,
        )

        row = results[0]
        self.assertIn("size", row)
        self.assertIn("min", row)
        self.assertIn("max", row)
        self.assertIn("mean", row)
        self.assertIn("median", row)

    def test_run_scaling_benchmark_size_recorded_correctly(self) -> None:
        sizes = [10, 50]

        def build_input(size: int) -> tuple[list[int], int]:
            return list(range(size)), size - 1

        results = run_scaling_benchmark(
            linear_search,
            sizes,
            build_input,
            repeats=2,
        )

        self.assertEqual(int(results[0]["size"]), 10)
        self.assertEqual(int(results[1]["size"]), 50)

    def test_format_seconds_returns_string(self) -> None:
        self.assertIsInstance(format_seconds(0.001), str)


if __name__ == "__main__":
    unittest.main()
