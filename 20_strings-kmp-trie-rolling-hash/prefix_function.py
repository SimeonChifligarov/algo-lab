"""
Prefix Function (LPS Array)

This module implements the prefix function, which is the core building
block for the KMP (Knuth–Morris–Pratt) string matching algorithm.

Definition:
    pi[i] = length of the longest proper prefix of s[:i+1]
            which is also a suffix of s[:i+1]

Key Idea:
    Instead of recomputing matches from scratch, we reuse previous
    information to "jump" efficiently after mismatches.
"""

from typing import List


def prefix_function(s: str) -> List[int]:
    """
    Compute the prefix function (pi array) for a string.

    Args:
        s: Input string

    Returns:
        List[int]: prefix array

    Example:
        s = "ababaca"
        pi = [0, 0, 1, 2, 3, 0, 1]
    """
    n = len(s)
    pi = [0] * n

    for i in range(1, n):
        j = pi[i - 1]

        # fallback using previously computed values
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]

        # extend match if possible
        if s[i] == s[j]:
            j += 1

        pi[i] = j

    return pi


def lps_array(pattern: str) -> List[int]:
    """
    Alias for prefix_function (KMP terminology).

    Args:
        pattern: Pattern string

    Returns:
        LPS array
    """
    return prefix_function(pattern)


def visualize_prefix_function(s: str) -> None:
    """
    Print a table showing how the prefix function behaves.

    Useful for understanding the algorithm step-by-step.
    """
    pi = prefix_function(s)

    print(f"\nString: {s}")
    print("-" * 40)
    print(f"{'Index':>5} | {'Char':>5} | {'pi[i]':>5}")
    print("-" * 40)

    for i, (ch, val) in enumerate(zip(s, pi)):
        print(f"{i:>5} | {ch:>5} | {val:>5}")

    print("-" * 40)


def debug_prefix_function(s: str) -> List[int]:
    """
    Verbose version showing internal state transitions.
    """
    n = len(s)
    pi = [0] * n

    print(f"\nDebugging prefix_function for: '{s}'\n")

    for i in range(1, n):
        j = pi[i - 1]
        print(f"[i={i}] comparing s[{i}]='{s[i]}'")

        while j > 0 and s[i] != s[j]:
            print(f"  mismatch with s[{j}]='{s[j]}', fallback -> pi[{j - 1}]={pi[j - 1]}")
            j = pi[j - 1]

        if s[i] == s[j]:
            j += 1
            print(f"  match with s[{j - 1}], increase j -> {j}")
        else:
            print("  no match, j stays 0")

        pi[i] = j
        print(f"  pi[{i}] = {j}\n")

    return pi


if __name__ == "__main__":
    # Simple manual runs (not formal tests)

    examples = [
        "a",
        "aaaa",
        "ababaca",
        "abcab",
        "ababcabab",
    ]

    for s in examples:
        visualize_prefix_function(s)

    # Debug one example in detail
    debug_prefix_function("ababaca")
