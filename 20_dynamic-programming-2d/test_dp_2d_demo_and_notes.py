import os
import sys

sys.path.append(os.path.dirname(__file__))

import io
import unittest
from contextlib import redirect_stdout

from dp_2d_demo_and_notes import (
    edit_distance_demo,
    grid_dp_demo,
    knapsack_demo,
    lcs_demo,
    main,
    print_notes,
    print_state_and_transition_notes,
    print_table_construction_notes,
)


class TestDP2DDemoAndNotes(unittest.TestCase):
    def capture_output(self, func):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            func()
        return buffer.getvalue()

    def test_print_notes_output(self):
        output = self.capture_output(print_notes)

        self.assertIn("=== 2D Dynamic Programming Notes ===", output)
        self.assertIn("dp[i][j]", output)
        self.assertIn("top: dp[i-1][j]", output)
        self.assertIn("left: dp[i][j-1]", output)
        self.assertIn("diagonal: dp[i-1][j-1]", output)

    def test_lcs_demo_output(self):
        output = self.capture_output(lcs_demo)

        self.assertIn("=== LCS Demo ===", output)
        self.assertIn("text1 =", output)
        self.assertIn("text2 =", output)
        self.assertIn("LCS length =", output)
        self.assertIn("One LCS", output)
        self.assertIn("LCS DP table:", output)

    def test_grid_dp_demo_output(self):
        output = self.capture_output(grid_dp_demo)

        self.assertIn("=== Grid DP Demo ===", output)
        self.assertIn("unique_paths(3, 4) =", output)
        self.assertIn("Unique Paths DP table:", output)
        self.assertIn("min_path_sum(grid) =", output)
        self.assertIn("Minimum Path Sum DP table:", output)

    def test_knapsack_demo_output(self):
        output = self.capture_output(knapsack_demo)

        self.assertIn("=== 0/1 Knapsack Demo ===", output)
        self.assertIn("values   =", output)
        self.assertIn("weights  =", output)
        self.assertIn("capacity =", output)
        self.assertIn("max value =", output)
        self.assertIn("Knapsack DP table:", output)

    def test_edit_distance_demo_output(self):
        output = self.capture_output(edit_distance_demo)

        self.assertIn("=== Edit Distance Demo ===", output)
        self.assertIn("word1 =", output)
        self.assertIn("word2 =", output)
        self.assertIn("edit distance =", output)
        self.assertIn("Edit Distance DP table:", output)

    def test_print_state_and_transition_notes_output(self):
        output = self.capture_output(print_state_and_transition_notes)

        self.assertIn("=== State and Transition Intuition ===", output)
        self.assertIn("LCS:", output)
        self.assertIn("Unique Paths:", output)
        self.assertIn("Minimum Path Sum:", output)
        self.assertIn("0/1 Knapsack:", output)
        self.assertIn("Edit Distance:", output)

    def test_print_table_construction_notes_output(self):
        output = self.capture_output(print_table_construction_notes)

        self.assertIn("=== Table Construction Notes ===", output)
        self.assertIn("row by row or column by column", output)
        self.assertIn("extra top row and left column", output)
        self.assertIn("dp[-1][-1] or dp[n][m]", output)
        self.assertIn("walk backward through the table", output)

    def test_main_runs_all_sections(self):
        output = self.capture_output(main)

        self.assertIn("=== 2D Dynamic Programming Notes ===", output)
        self.assertIn("=== LCS Demo ===", output)
        self.assertIn("=== Grid DP Demo ===", output)
        self.assertIn("=== 0/1 Knapsack Demo ===", output)
        self.assertIn("=== Edit Distance Demo ===", output)
        self.assertIn("=== State and Transition Intuition ===", output)
        self.assertIn("=== Table Construction Notes ===", output)

    def test_main_produces_non_empty_output(self):
        output = self.capture_output(main)
        self.assertTrue(len(output.strip()) > 0)


if __name__ == "__main__":
    unittest.main()
