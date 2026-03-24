"""
A small driver / notes file for 1D dynamic programming.

This file ties together:
- Fibonacci
- Climbing Stairs
- House Robber
- Kadane's Algorithm

It also explains:
- what a DP state means
- how transitions are formed
- when space optimization is possible
"""

from fibonacci_dp import (
    fibonacci_bottom_up,
    fibonacci_space_optimized,
    fibonacci_top_down,
)
from climbing_stairs import (
    climbing_stairs_bottom_up,
    climbing_stairs_space_optimized,
    climbing_stairs_top_down,
)
from house_robber_and_kadane import (
    house_robber,
    house_robber_with_table,
    kadane_max_subarray,
    kadane_with_indices,
)


def print_notes() -> None:
    """
    Print short conceptual notes for 1D dynamic programming.
    """
    print("=== 1D Dynamic Programming Notes ===")
    print("1. Define a state that captures the answer to a smaller subproblem.")
    print("2. Write a transition that builds the current state from earlier states.")
    print("3. Set base cases carefully.")
    print("4. Compute answers either top-down (memoization) or bottom-up (tabulation).")
    print("5. If each state depends on only a few previous states, space can often be reduced.")
    print()


def fibonacci_demo() -> None:
    """
    Demonstrate the three Fibonacci implementations.
    """
    print("=== Fibonacci Demo ===")
    n = 10
    print(f"n = {n}")
    print(f"top-down:        {fibonacci_top_down(n)}")
    print(f"bottom-up:       {fibonacci_bottom_up(n)}")
    print(f"space-optimized: {fibonacci_space_optimized(n)}")
    print()


def climbing_stairs_demo() -> None:
    """
    Demonstrate the three Climbing Stairs implementations.
    """
    print("=== Climbing Stairs Demo ===")
    n = 5
    print(f"n = {n}")
    print(f"top-down:        {climbing_stairs_top_down(n)}")
    print(f"bottom-up:       {climbing_stairs_bottom_up(n)}")
    print(f"space-optimized: {climbing_stairs_space_optimized(n)}")
    print()


def house_robber_demo() -> None:
    """
    Demonstrate House Robber.
    """
    print("=== House Robber Demo ===")
    houses = [2, 7, 9, 3, 1]
    print("houses =", houses)
    print("with table:      ", house_robber_with_table(houses))
    print("space-optimized: ", house_robber(houses))
    print()


def kadane_demo() -> None:
    """
    Demonstrate Kadane's Algorithm.
    """
    print("=== Kadane's Algorithm Demo ===")
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print("nums =", nums)
    print("max subarray sum =", kadane_max_subarray(nums))

    max_sum, start, end = kadane_with_indices(nums)
    print("with indices     =", (max_sum, start, end))
    print("best subarray    =", nums[start:end + 1])
    print()


def print_state_and_transition_notes() -> None:
    """
    Print notes focused on state and transition design.
    """
    print("=== State and Transition Intuition ===")
    print("Fibonacci:")
    print("  state: fib(i) = ith Fibonacci number")
    print("  transition: fib(i) = fib(i-1) + fib(i-2)")
    print()

    print("Climbing Stairs:")
    print("  state: ways(i) = number of ways to reach step i")
    print("  transition: ways(i) = ways(i-1) + ways(i-2)")
    print()

    print("House Robber:")
    print("  state: best(i) = max money from houses[0..i]")
    print("  transition: best(i) = max(best(i-1), best(i-2) + nums[i])")
    print()

    print("Kadane:")
    print("  state: best_ending_here(i) = best subarray sum ending at i")
    print("  transition: best_ending_here(i) = max(nums[i], best_ending_here(i-1) + nums[i])")
    print()


def print_space_optimization_notes() -> None:
    """
    Print notes about space optimization in 1D DP.
    """
    print("=== Space Optimization Notes ===")
    print("If dp[i] depends only on dp[i-1], dp[i-2], or a small fixed number")
    print("of earlier states, we do not need the full DP table.")
    print()
    print("Examples:")
    print("  - Fibonacci uses only the previous two values.")
    print("  - Climbing Stairs uses only the previous two values.")
    print("  - House Robber uses only the previous two states.")
    print("  - Kadane uses only the previous best-ending-here value and the global best.")
    print()


def main() -> None:
    print_notes()
    fibonacci_demo()
    climbing_stairs_demo()
    house_robber_demo()
    kadane_demo()
    print_state_and_transition_notes()
    print_space_optimization_notes()


if __name__ == "__main__":
    main()
