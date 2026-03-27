"""
Learn 2D dynamic programming through:
- 0/1 Knapsack (table-based DP)
- Edit Distance (Levenshtein distance)

Main DP ideas:
- 2D state definitions
- building tables row by row
- understanding transitions from previous rows/columns
"""


def knapsack_01(values: list[int], weights: list[int], capacity: int) -> int:
    """
    Solve the 0/1 Knapsack problem using a 2D DP table.

    Args:
        values:
            value of each item
        weights:
            weight of each item
        capacity:
            maximum capacity of the knapsack

    Returns:
        maximum achievable value
    """
    _validate_knapsack_inputs(values, weights, capacity)

    n = len(values)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        value = values[i - 1]
        weight = weights[i - 1]

        for w in range(capacity + 1):
            if weight <= w:
                dp[i][w] = max(
                    dp[i - 1][w],  # skip item
                    dp[i - 1][w - weight] + value  # take item
                )
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]


def build_knapsack_table(values: list[int], weights: list[int], capacity: int) -> list[list[int]]:
    """
    Return the full DP table for the 0/1 Knapsack problem.
    """
    _validate_knapsack_inputs(values, weights, capacity)

    n = len(values)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        value = values[i - 1]
        weight = weights[i - 1]

        for w in range(capacity + 1):
            if weight <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weight] + value)
            else:
                dp[i][w] = dp[i - 1][w]

    return dp


def edit_distance(word1: str, word2: str) -> int:
    """
    Compute the Levenshtein distance between two strings.

    Operations allowed:
    - insert
    - delete
    - replace
    """
    dp = build_edit_distance_table(word1, word2)
    return dp[len(word1)][len(word2)]


def build_edit_distance_table(word1: str, word2: str) -> list[list[int]]:
    """
    Build and return the DP table for edit distance.
    """
    rows = len(word1) + 1
    cols = len(word2) + 1

    dp = [[0] * cols for _ in range(rows)]

    # Base cases
    for i in range(rows):
        dp[i][0] = i

    for j in range(cols):
        dp[0][j] = j

    # Fill table
    for i in range(1, rows):
        for j in range(1, cols):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],  # delete
                    dp[i][j - 1],  # insert
                    dp[i - 1][j - 1],  # replace
                )

    return dp


def _validate_knapsack_inputs(values: list[int], weights: list[int], capacity: int) -> None:
    if len(values) != len(weights):
        raise ValueError("values and weights must have the same length")

    if capacity < 0:
        raise ValueError("capacity must be non-negative")

    for w in weights:
        if w < 0:
            raise ValueError("weights must be non-negative")


def print_table(table: list[list[int]], title: str) -> None:
    """
    Print a DP table in a readable format.
    """
    print(title)
    for row in table:
        print("  ".join(str(x) for x in row))


def demo() -> None:
    print("=== 0/1 Knapsack Demo ===")

    values = [60, 100, 120]
    weights = [10, 20, 30]
    capacity = 50

    print("max value =", knapsack_01(values, weights, capacity))
    print()
    print_table(
        build_knapsack_table(values, weights, capacity),
        "Knapsack DP table:",
    )
    print()

    print("=== Edit Distance Demo ===")

    word1 = "kitten"
    word2 = "sitting"

    print(f"edit_distance('{word1}', '{word2}') =", edit_distance(word1, word2))
    print()
    print_table(
        build_edit_distance_table(word1, word2),
        "Edit Distance DP table:",
    )


if __name__ == "__main__":
    demo()
