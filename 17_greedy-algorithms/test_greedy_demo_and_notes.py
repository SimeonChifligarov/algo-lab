import os
import sys

sys.path.append(os.path.dirname(__file__))

import io
import unittest
from contextlib import redirect_stdout

from greedy_demo_and_notes import (
    activity_selection_demo,
    correctness_notes,
    fractional_knapsack_demo,
    greedy_notes,
    huffman_demo,
    main,
)


class TestGreedyDemoAndNotes(unittest.TestCase):
    def capture_output(self, func):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            func()
        return buffer.getvalue()

    def test_greedy_notes_output(self):
        output = self.capture_output(greedy_notes)

        self.assertIn("=== Greedy Algorithm Notes ===", output)
        self.assertIn("local choice", output)
        self.assertIn("exchange argument", output)

    def test_activity_selection_demo_output(self):
        output = self.capture_output(activity_selection_demo)

        self.assertIn("=== Activity Selection Demo ===", output)
        self.assertIn("Selected activities:", output)
        self.assertIn("Total selected:", output)

    def test_fractional_knapsack_demo_output(self):
        output = self.capture_output(fractional_knapsack_demo)

        self.assertIn("=== Fractional Knapsack Demo ===", output)
        self.assertIn("Chosen items:", output)
        self.assertIn("Total value:", output)

    def test_huffman_demo_output(self):
        output = self.capture_output(huffman_demo)

        self.assertIn("=== Huffman Coding Demo ===", output)
        self.assertIn("Huffman Codes:", output)
        self.assertIn("Original:", output)
        self.assertIn("Encoded:", output)
        self.assertIn("Decoded:", output)

    def test_correctness_notes_output(self):
        output = self.capture_output(correctness_notes)

        self.assertIn("=== Correctness Intuition ===", output)
        self.assertIn("Activity Selection:", output)
        self.assertIn("Fractional Knapsack:", output)
        self.assertIn("Huffman Coding:", output)

    def test_main_runs_all_sections(self):
        output = self.capture_output(main)

        self.assertIn("=== Greedy Algorithm Notes ===", output)
        self.assertIn("=== Activity Selection Demo ===", output)
        self.assertIn("=== Fractional Knapsack Demo ===", output)
        self.assertIn("=== Huffman Coding Demo ===", output)
        self.assertIn("=== Correctness Intuition ===", output)

    def test_main_produces_non_empty_output(self):
        output = self.capture_output(main)

        self.assertTrue(len(output.strip()) > 0)


if __name__ == "__main__":
    unittest.main()
