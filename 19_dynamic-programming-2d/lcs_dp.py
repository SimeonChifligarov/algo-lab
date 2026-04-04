"""
Learn 2D dynamic programming through the Longest Common Subsequence (LCS) problem.

Problem:
Given two strings, find the length of their longest common subsequence.
A subsequence does not need to be contiguous, but order must be preserved.

This file includes:
- LCS length using a 2D DP table
- reconstruction of one actual LCS string
- a small demo

Main DP ideas:
- state:
    dp[i][j] = length of the LCS of text1[:i] and text2[:j]
- transition:
    if text1[i - 1] == text2[j - 1]:
        dp[i][j] = dp[i - 1][j - 1] + 1
    else:
        dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
- base case:
    dp[0][j] = 0 and dp[i][0] = 0
"""


def lcs_length(text1: str, text2: str) -> int:
    """
    Return the length of the longest common subsequence of text1 and text2.
    """
    dp = build_lcs_table(text1, text2)
    return dp[len(text1)][len(text2)]


def build_lcs_table(text1: str, text2: str) -> list[list[int]]:
    """
    Build and return the 2D DP table for LCS.

    dp[i][j] represents the LCS length of text1[:i] and text2[:j].
    """
    rows = len(text1) + 1
    cols = len(text2) + 1

    dp = [[0] * cols for _ in range(rows)]

    for i in range(1, rows):
        for j in range(1, cols):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp


def lcs_string(text1: str, text2: str) -> str:
    """
    Reconstruct and return one longest common subsequence.

    Note:
    There may be multiple valid LCS strings with the same maximum length.
    This function returns one of them.
    """
    dp = build_lcs_table(text1, text2)

    i = len(text1)
    j = len(text2)
    result = []

    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            result.append(text1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    result.reverse()
    return "".join(result)


def print_lcs_table(text1: str, text2: str) -> None:
    """
    Print the LCS DP table in a readable format.
    """
    dp = build_lcs_table(text1, text2)

    print("LCS DP table:")
    print("    ", "  ".join(["_"] + list(text2)))

    for i, row in enumerate(dp):
        row_label = "_" if i == 0 else text1[i - 1]
        print(f"{row_label}   " + "  ".join(str(value) for value in row))


def demo() -> None:
    print("=== LCS DP Demo ===")

    text1 = "abcde"
    text2 = "ace"

    print("text1 =", text1)
    print("text2 =", text2)
    print("LCS length =", lcs_length(text1, text2))
    print("One LCS    =", lcs_string(text1, text2))
    print()

    print_lcs_table(text1, text2)


if __name__ == "__main__":
    demo()
