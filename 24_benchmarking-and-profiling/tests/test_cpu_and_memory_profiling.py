"""
Unit tests for cpu_and_memory_profiling.py

These tests focus on correctness and light smoke testing.
They intentionally avoid asserting exact profiling output or exact memory values.
"""
import os
import sys

sys.path.append(os.path.dirname(__file__))

import io
import unittest
from contextlib import redirect_stdout

from ..cpu_and_memory_profiling import (
    allocate_memory,
    fast_fibonacci,
    profile_cpu,
    profile_memory,
    slow_fibonacci,
)


class TestCpuAndMemoryProfiling(unittest.TestCase):
    def test_slow_fibonacci_base_cases(self) -> None:
        self.assertEqual(slow_fibonacci(0), 0)
        self.assertEqual(slow_fibonacci(1), 1)

    def test_fast_fibonacci_base_cases(self) -> None:
        self.assertEqual(fast_fibonacci(0), 0)
        self.assertEqual(fast_fibonacci(1), 1)

    def test_slow_and_fast_fibonacci_match(self) -> None:
        for n in range(10):
            self.assertEqual(slow_fibonacci(n), fast_fibonacci(n))

    def test_fast_fibonacci_known_value(self) -> None:
        self.assertEqual(fast_fibonacci(10), 55)

    def test_allocate_memory_returns_expected_list(self) -> None:
        self.assertEqual(allocate_memory(5), [0, 1, 4, 9, 16])

    def test_allocate_memory_empty(self) -> None:
        self.assertEqual(allocate_memory(0), [])

    def test_profile_cpu_runs_without_error(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            profile_cpu(fast_fibonacci, 10)

        output = buffer.getvalue()
        self.assertIn("CPU Profile", output)
        self.assertIn("fast_fibonacci", output)

    def test_profile_memory_runs_without_error(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            profile_memory(allocate_memory, 100)

        output = buffer.getvalue()
        self.assertIn("Memory Profile", output)
        self.assertIn("Current memory usage", output)
        self.assertIn("Peak memory usage", output)


if __name__ == "__main__":
    unittest.main()
