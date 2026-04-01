"""
Bit counting and classic bit tricks.

This module focuses on:
- Counting set bits (multiple methods)
- Brian Kernighan’s algorithm
- Power of two checks
- Related useful bit tricks

These are extremely common in interviews and optimization problems.
"""

from typing import List


def count_set_bits_naive(n: int) -> int:
    """
    Count set bits using simple shifting.

    Args:
        n: Non-negative integer

    Returns:
        Number of 1 bits

    Time Complexity:
        O(number of bits)
    """
    if n < 0:
        raise ValueError("Only non-negative integers are supported")

    count = 0
    while n > 0:
        count += n & 1
        n >>= 1
    return count


def count_set_bits_kernighan(n: int) -> int:
    """
    Count set bits using Brian Kernighan’s algorithm.

    Key idea:
        Repeatedly remove the lowest set bit.

        n = n & (n - 1)

    Args:
        n: Non-negative integer

    Returns:
        Number of set bits

    Time Complexity:
        O(number of set bits)
    """
    if n < 0:
        raise ValueError("Only non-negative integers are supported")

    count = 0
    while n:
        n &= n - 1
        count += 1
    return count


def count_set_bits_builtin(n: int) -> int:
    """
    Count set bits using Python built-in.

    Equivalent to C++ __builtin_popcount.
    """
    if n < 0:
        raise ValueError("Only non-negative integers are supported")

    return bin(n).count("1")


def is_power_of_two(n: int) -> bool:
    """
    Check if n is a power of two.

    Key identity:
        n & (n - 1) == 0  (only for powers of two)

    Args:
        n: integer

    Returns:
        True if n is a power of two, else False
    """
    if n <= 0:
        return False
    return (n & (n - 1)) == 0


def next_power_of_two(n: int) -> int:
    """
    Return the smallest power of two >= n.

    Args:
        n: positive integer

    Returns:
        Next power of two

    Example:
        n = 5 -> 8
        n = 8 -> 8
    """
    if n <= 0:
        raise ValueError("n must be positive")

    if is_power_of_two(n):
        return n

    power = 1
    while power < n:
        power <<= 1
    return power


def previous_power_of_two(n: int) -> int:
    """
    Return the largest power of two <= n.

    Args:
        n: positive integer

    Returns:
        Largest power of two <= n
    """
    if n <= 0:
        raise ValueError("n must be positive")

    power = 1
    while (power << 1) <= n:
        power <<= 1
    return power


def count_bits_upto(n: int) -> List[int]:
    """
    Compute number of set bits for all numbers from 0 to n.

    Uses DP relation:
        bits[i] = bits[i >> 1] + (i & 1)

    Args:
        n: non-negative integer

    Returns:
        List of size (n+1) with bit counts
    """
    if n < 0:
        raise ValueError("n must be non-negative")

    bits = [0] * (n + 1)

    for i in range(1, n + 1):
        bits[i] = bits[i >> 1] + (i & 1)

    return bits


def parity(n: int) -> int:
    """
    Return parity of n (0 if even number of bits, 1 if odd).

    Uses Kernighan’s trick.
    """
    if n < 0:
        raise ValueError("Only non-negative integers are supported")

    result = 0
    while n:
        result ^= 1
        n &= n - 1
    return result


def explain_bit_counting(n: int) -> None:
    """
    Print a comparison of different bit counting approaches.
    """
    if n < 0:
        raise ValueError("Only non-negative integers are supported")

    print("\nBit Counting Explanation")
    print("=" * 60)
    print(f"n = {n}")
    print(f"binary = {bin(n)[2:]}")
    print("-" * 60)

    print(f"naive count        -> {count_set_bits_naive(n)}")
    print(f"kernighan count    -> {count_set_bits_kernighan(n)}")
    print(f"builtin count      -> {count_set_bits_builtin(n)}")

    print("-" * 60)
    print(f"is power of two    -> {is_power_of_two(n)}")

    if n > 0:
        print(f"next power of two  -> {next_power_of_two(n)}")
        print(f"prev power of two  -> {previous_power_of_two(n)}")

    print(f"parity             -> {parity(n)}")


def explain_kernighan_steps(n: int) -> None:
    """
    Show step-by-step how Kernighan’s algorithm removes bits.
    """
    if n < 0:
        raise ValueError("Only non-negative integers are supported")

    print("\nKernighan Algorithm Steps")
    print("=" * 60)

    step = 0
    while n:
        print(f"step {step}: n = {n} ({bin(n)[2:]})")
        n = n & (n - 1)
        step += 1

    print(f"step {step}: n = 0")


if __name__ == "__main__":
    values = [0, 1, 5, 8, 13, 42]

    print("Bit Counting Demo")
    print("=" * 60)

    for v in values:
        explain_bit_counting(v)

    print("\nDP bit counts up to 10")
    print("=" * 60)
    print(count_bits_upto(10))

    explain_kernighan_steps(13)
