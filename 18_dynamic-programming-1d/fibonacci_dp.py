"""
Learn 1D dynamic programming through Fibonacci.

This file includes:
- top-down Fibonacci with memoization
- bottom-up Fibonacci with a DP table
- bottom-up Fibonacci with space optimization

Main DP ideas:
- state: fib(n) = nth Fibonacci number
- transition: fib(n) = fib(n - 1) + fib(n - 2)
- base cases: fib(0) = 0, fib(1) = 1
"""


def fibonacci_top_down(n: int, memo: dict[int, int] | None = None) -> int:
    """
    Compute the nth Fibonacci number using top-down DP (memoization).

    Args:
        n:
            Non-negative index in the Fibonacci sequence.
        memo:
            Optional dictionary used for memoization.

    Returns:
        The nth Fibonacci number.

    Raises:
        ValueError:
            If n is negative.
    """
    _validate_n(n)

    if memo is None:
        memo = {}

    if n in memo:
        return memo[n]

    if n == 0:
        return 0
    if n == 1:
        return 1

    memo[n] = fibonacci_top_down(n - 1, memo) + fibonacci_top_down(n - 2, memo)
    return memo[n]


def fibonacci_bottom_up(n: int) -> int:
    """
    Compute the nth Fibonacci number using bottom-up DP.

    Builds a DP table from 0 up to n.
    """
    _validate_n(n)

    if n == 0:
        return 0
    if n == 1:
        return 1

    dp = [0] * (n + 1)
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]


def fibonacci_space_optimized(n: int) -> int:
    """
    Compute the nth Fibonacci number using bottom-up DP
    with O(1) extra space.
    """
    _validate_n(n)

    if n == 0:
        return 0
    if n == 1:
        return 1

    prev2 = 0
    prev1 = 1

    for _ in range(2, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current

    return prev1


def _validate_n(n: int) -> None:
    if n < 0:
        raise ValueError("n must be non-negative")


def demo() -> None:
    print("=== Fibonacci DP Demo ===")

    n = 10

    print(f"fibonacci_top_down({n}) = {fibonacci_top_down(n)}")
    print(f"fibonacci_bottom_up({n}) = {fibonacci_bottom_up(n)}")
    print(f"fibonacci_space_optimized({n}) = {fibonacci_space_optimized(n)}")


if __name__ == "__main__":
    demo()
