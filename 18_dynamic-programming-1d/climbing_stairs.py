"""
Learn 1D dynamic programming through the Climbing Stairs problem.

Problem:
You are climbing a staircase with n steps.
Each time, you can climb either 1 step or 2 steps.
How many distinct ways are there to reach the top?

This file includes:
- top-down solution with memoization
- bottom-up solution with a DP table
- space-optimized bottom-up solution

Main DP ideas:
- state: ways(i) = number of ways to reach step i
- transition: ways(i) = ways(i - 1) + ways(i - 2)
- base cases:
    ways(0) = 1   (one way to stay at the ground)
    ways(1) = 1
"""


def climbing_stairs_top_down(n: int, memo: dict[int, int] | None = None) -> int:
    """
    Compute the number of distinct ways to climb n stairs
    using top-down DP (memoization).

    Args:
        n:
            Number of stairs, must be non-negative.
        memo:
            Optional dictionary used for memoization.

    Returns:
        Number of distinct ways to reach step n.

    Raises:
        ValueError:
            If n is negative.
    """
    _validate_n(n)

    if memo is None:
        memo = {}

    if n in memo:
        return memo[n]

    if n == 0 or n == 1:
        return 1

    memo[n] = (
            climbing_stairs_top_down(n - 1, memo)
            + climbing_stairs_top_down(n - 2, memo)
    )
    return memo[n]


def climbing_stairs_bottom_up(n: int) -> int:
    """
    Compute the number of distinct ways to climb n stairs
    using bottom-up DP with a table.
    """
    _validate_n(n)

    if n == 0 or n == 1:
        return 1

    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]


def climbing_stairs_space_optimized(n: int) -> int:
    """
    Compute the number of distinct ways to climb n stairs
    using bottom-up DP with O(1) extra space.
    """
    _validate_n(n)

    if n == 0 or n == 1:
        return 1

    prev2 = 1  # ways(0)
    prev1 = 1  # ways(1)

    for _ in range(2, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current

    return prev1


def _validate_n(n: int) -> None:
    if n < 0:
        raise ValueError("n must be non-negative")


def demo() -> None:
    print("=== Climbing Stairs DP Demo ===")

    n = 5

    print(f"climbing_stairs_top_down({n}) = {climbing_stairs_top_down(n)}")
    print(f"climbing_stairs_bottom_up({n}) = {climbing_stairs_bottom_up(n)}")
    print(
        f"climbing_stairs_space_optimized({n}) = "
        f"{climbing_stairs_space_optimized(n)}"
    )


if __name__ == "__main__":
    demo()
