import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import io
import unittest
from contextlib import redirect_stdout

from ..dp_1d_demo_and_notes import (
    climbing_stairs_demo,
    fibonacci_demo,
    house_robber_demo,
    kadane_demo,
    main,
    print_notes,
    print_space_optimization_notes,
    print_state_and_transition_notes,
)


class TestDP1DDemoAndNotes(unittest.TestCase):
    def capture_output(self, func):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            func()
        return buffer.getvalue()

    def test_print_notes_output(self):
        output = self.capture_output(print_notes)

        self.assertIn("=== 1D Dynamic Programming Notes ===", output)
        self.assertIn("state", output)
        self.assertIn("transition", output)
        self.assertIn("memoization", output)
        self.assertIn("space can often be reduced", output)

    def test_fibonacci_demo_output(self):
        output = self.capture_output(fibonacci_demo)

        self.assertIn("=== Fibonacci Demo ===", output)
        self.assertIn("n = 10", output)
        self.assertIn("top-down:", output)
        self.assertIn("bottom-up:", output)
        self.assertIn("space-optimized:", output)

    def test_climbing_stairs_demo_output(self):
        output = self.capture_output(climbing_stairs_demo)

        self.assertIn("=== Climbing Stairs Demo ===", output)
        self.assertIn("n = 5", output)
        self.assertIn("top-down:", output)
        self.assertIn("bottom-up:", output)
        self.assertIn("space-optimized:", output)

    def test_house_robber_demo_output(self):
        output = self.capture_output(house_robber_demo)

        self.assertIn("=== House Robber Demo ===", output)
        self.assertIn("houses =", output)
        self.assertIn("with table:", output)
        self.assertIn("space-optimized:", output)

    def test_kadane_demo_output(self):
        output = self.capture_output(kadane_demo)

        self.assertIn("=== Kadane's Algorithm Demo ===", output)
        self.assertIn("nums =", output)
        self.assertIn("max subarray sum =", output)
        self.assertIn("with indices     =", output)
        self.assertIn("best subarray    =", output)

    def test_print_state_and_transition_notes_output(self):
        output = self.capture_output(print_state_and_transition_notes)

        self.assertIn("=== State and Transition Intuition ===", output)
        self.assertIn("Fibonacci:", output)
        self.assertIn("Climbing Stairs:", output)
        self.assertIn("House Robber:", output)
        self.assertIn("Kadane:", output)
        self.assertIn("transition:", output)

    def test_print_space_optimization_notes_output(self):
        output = self.capture_output(print_space_optimization_notes)

        self.assertIn("=== Space Optimization Notes ===", output)
        self.assertIn("dp[i] depends only on dp[i-1], dp[i-2]", output)
        self.assertIn("Fibonacci", output)
        self.assertIn("Climbing Stairs", output)
        self.assertIn("House Robber", output)
        self.assertIn("Kadane", output)

    def test_main_runs_all_sections(self):
        output = self.capture_output(main)

        self.assertIn("=== 1D Dynamic Programming Notes ===", output)
        self.assertIn("=== Fibonacci Demo ===", output)
        self.assertIn("=== Climbing Stairs Demo ===", output)
        self.assertIn("=== House Robber Demo ===", output)
        self.assertIn("=== Kadane's Algorithm Demo ===", output)
        self.assertIn("=== State and Transition Intuition ===", output)
        self.assertIn("=== Space Optimization Notes ===", output)

    def test_main_produces_non_empty_output(self):
        output = self.capture_output(main)
        self.assertTrue(len(output.strip()) > 0)


if __name__ == "__main__":
    unittest.main()
