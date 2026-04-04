"""
Learn 2D dynamic programming through grid-based problems.

This file includes:
- Unique Paths
- Minimum Path Sum

Main DP ideas:
- state:
    dp[r][c] stores the answer for cell (r, c)
- transition:
    build each cell from top / left neighbors
- base cases:
    first row and first column are often initialized separately
"""


def unique_paths(rows: int, cols: int) -> int:
    """
    Return the number of unique paths from top-left to bottom-right
    in a rows x cols grid, moving only right or down.
    """
    _validate_dimensions(rows, cols)

    dp = [[0] * cols for _ in range(rows)]

    for r in range(rows):
        dp[r][0] = 1

    for c in range(cols):
        dp[0][c] = 1

    for r in range(1, rows):
        for c in range(1, cols):
            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]

    return dp[rows - 1][cols - 1]


def build_unique_paths_table(rows: int, cols: int) -> list[list[int]]:
    """
    Build and return the DP table for the Unique Paths problem.
    """
    _validate_dimensions(rows, cols)

    dp = [[0] * cols for _ in range(rows)]

    for r in range(rows):
        dp[r][0] = 1

    for c in range(cols):
        dp[0][c] = 1

    for r in range(1, rows):
        for c in range(1, cols):
            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]

    return dp


def min_path_sum(grid: list[list[int]]) -> int:
    """
    Return the minimum path sum from top-left to bottom-right
    in a grid of non-negative numbers, moving only right or down.
    """
    _validate_grid(grid)

    rows = len(grid)
    cols = len(grid[0])

    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = grid[0][0]

    for c in range(1, cols):
        dp[0][c] = dp[0][c - 1] + grid[0][c]

    for r in range(1, rows):
        dp[r][0] = dp[r - 1][0] + grid[r][0]

    for r in range(1, rows):
        for c in range(1, cols):
            dp[r][c] = min(dp[r - 1][c], dp[r][c - 1]) + grid[r][c]

    return dp[rows - 1][cols - 1]


def build_min_path_sum_table(grid: list[list[int]]) -> list[list[int]]:
    """
    Build and return the DP table for Minimum Path Sum.
    """
    _validate_grid(grid)

    rows = len(grid)
    cols = len(grid[0])

    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = grid[0][0]

    for c in range(1, cols):
        dp[0][c] = dp[0][c - 1] + grid[0][c]

    for r in range(1, rows):
        dp[r][0] = dp[r - 1][0] + grid[r][0]

    for r in range(1, rows):
        for c in range(1, cols):
            dp[r][c] = min(dp[r - 1][c], dp[r][c - 1]) + grid[r][c]

    return dp


def _validate_dimensions(rows: int, cols: int) -> None:
    if rows <= 0 or cols <= 0:
        raise ValueError("rows and cols must both be positive")


def _validate_grid(grid: list[list[int]]) -> None:
    if not grid or not grid[0]:
        raise ValueError("grid must be non-empty")

    cols = len(grid[0])

    for row in grid:
        if len(row) != cols:
            raise ValueError("grid must be rectangular")
        for value in row:
            if value < 0:
                raise ValueError("grid values must be non-negative")


def print_table(table: list[list[int]], title: str) -> None:
    """
    Print a DP table in a readable format.
    """
    print(title)
    for row in table:
        print("  ".join(str(value) for value in row))


def demo() -> None:
    print("=== Grid DP Demo ===")

    rows, cols = 3, 4
    print(f"unique_paths({rows}, {cols}) =", unique_paths(rows, cols))
    print()
    print_table(build_unique_paths_table(rows, cols), "Unique Paths DP table:")
    print()

    grid = [
        [1, 3, 1],
        [1, 5, 1],
        [4, 2, 1],
    ]
    print("min_path_sum(grid) =", min_path_sum(grid))
    print()
    print_table(build_min_path_sum_table(grid), "Minimum Path Sum DP table:")


if __name__ == "__main__":
    demo()
