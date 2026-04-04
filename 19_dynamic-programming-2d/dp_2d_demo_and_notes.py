"""
A small driver / notes file for 2D dynamic programming.

This file ties together:
- Longest Common Subsequence (LCS)
- Grid DP (Unique Paths, Minimum Path Sum)
- 0/1 Knapsack
- Edit Distance

It also explains:
- what a 2D DP state means
- how 2D transitions are formed
- how tables are constructed and interpreted
"""

from lcs_dp import lcs_length, lcs_string, print_lcs_table
from grid_dp import (
    build_min_path_sum_table,
    build_unique_paths_table,
    min_path_sum,
    print_table as print_grid_table,
    unique_paths,
)
from knapsack_and_edit_distance import (
    build_edit_distance_table,
    build_knapsack_table,
    edit_distance,
    knapsack_01,
    print_table as print_dp_table,
)


def print_notes() -> None:
    """
    Print short conceptual notes for 2D dynamic programming.
    """
    print("=== 2D Dynamic Programming Notes ===")
    print("1. Define a state using two indices, often dp[i][j].")
    print("2. Each cell usually depends on neighboring cells such as:")
    print("   - top: dp[i-1][j]")
    print("   - left: dp[i][j-1]")
    print("   - diagonal: dp[i-1][j-1]")
    print("3. Add an extra row/column when base cases are easier that way.")
    print("4. Fill the table in an order that guarantees dependencies are already solved.")
    print("5. The final answer is often in the bottom-right corner.")
    print()


def lcs_demo() -> None:
    """
    Demonstrate LCS.
    """
    print("=== LCS Demo ===")
    text1 = "abcde"
    text2 = "ace"

    print("text1 =", text1)
    print("text2 =", text2)
    print("LCS length =", lcs_length(text1, text2))
    print("One LCS    =", lcs_string(text1, text2))
    print()
    print_lcs_table(text1, text2)
    print()


def grid_dp_demo() -> None:
    """
    Demonstrate grid-based 2D DP problems.
    """
    print("=== Grid DP Demo ===")

    rows, cols = 3, 4
    print(f"unique_paths({rows}, {cols}) =", unique_paths(rows, cols))
    print()
    print_grid_table(build_unique_paths_table(rows, cols), "Unique Paths DP table:")
    print()

    grid = [
        [1, 3, 1],
        [1, 5, 1],
        [4, 2, 1],
    ]
    print("min_path_sum(grid) =", min_path_sum(grid))
    print()
    print_grid_table(build_min_path_sum_table(grid), "Minimum Path Sum DP table:")
    print()


def knapsack_demo() -> None:
    """
    Demonstrate 0/1 Knapsack.
    """
    print("=== 0/1 Knapsack Demo ===")

    values = [60, 100, 120]
    weights = [10, 20, 30]
    capacity = 50

    print("values   =", values)
    print("weights  =", weights)
    print("capacity =", capacity)
    print("max value =", knapsack_01(values, weights, capacity))
    print()
    print_dp_table(
        build_knapsack_table(values, weights, capacity),
        "Knapsack DP table:",
    )
    print()


def edit_distance_demo() -> None:
    """
    Demonstrate Edit Distance.
    """
    print("=== Edit Distance Demo ===")

    word1 = "kitten"
    word2 = "sitting"

    print("word1 =", word1)
    print("word2 =", word2)
    print("edit distance =", edit_distance(word1, word2))
    print()
    print_dp_table(
        build_edit_distance_table(word1, word2),
        "Edit Distance DP table:",
    )
    print()


def print_state_and_transition_notes() -> None:
    """
    Print notes focused on 2D state and transition design.
    """
    print("=== State and Transition Intuition ===")

    print("LCS:")
    print("  state: dp[i][j] = LCS length of text1[:i] and text2[:j]")
    print("  transitions:")
    print("    if characters match: dp[i][j] = dp[i-1][j-1] + 1")
    print("    else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])")
    print()

    print("Unique Paths:")
    print("  state: dp[r][c] = number of ways to reach cell (r, c)")
    print("  transition: dp[r][c] = dp[r-1][c] + dp[r][c-1]")
    print()

    print("Minimum Path Sum:")
    print("  state: dp[r][c] = minimum cost to reach cell (r, c)")
    print("  transition: dp[r][c] = min(dp[r-1][c], dp[r][c-1]) + grid[r][c]")
    print()

    print("0/1 Knapsack:")
    print("  state: dp[i][w] = best value using first i items with capacity w")
    print("  transition:")
    print("    skip item i: dp[i-1][w]")
    print("    take item i: dp[i-1][w-weight[i-1]] + value[i-1]")
    print()

    print("Edit Distance:")
    print("  state: dp[i][j] = minimum edits to convert word1[:i] into word2[:j]")
    print("  transitions come from:")
    print("    delete   -> dp[i-1][j]")
    print("    insert   -> dp[i][j-1]")
    print("    replace  -> dp[i-1][j-1]")
    print()


def print_table_construction_notes() -> None:
    """
    Print notes about table construction in 2D DP.
    """
    print("=== Table Construction Notes ===")
    print("A 2D DP table is usually filled row by row or column by column.")
    print("The fill order must ensure dependencies are already available.")
    print()
    print("Common patterns:")
    print("  - Use an extra top row and left column for empty-prefix base cases.")
    print("  - Initialize first row / first column separately in grid problems.")
    print("  - Put the final answer in dp[-1][-1] or dp[n][m].")
    print()
    print("To reconstruct a solution, walk backward through the table")
    print("and follow the choices that created the optimal value.")
    print()


def main() -> None:
    print_notes()
    lcs_demo()
    grid_dp_demo()
    knapsack_demo()
    edit_distance_demo()
    print_state_and_transition_notes()
    print_table_construction_notes()


if __name__ == "__main__":
    main()
