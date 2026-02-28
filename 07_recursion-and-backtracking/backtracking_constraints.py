"""
Recursion & Backtracking — constraint solving + pruning (Part 3/4)

Focus:
- N-Queens (classic constraint satisfaction)
- Sudoku-like "pruning mindset" helpers:
  - generate_parentheses (balanced parentheses; early prune)
  - word_search (DFS with backtracking + early exits)

These showcase:
- tracking constraints in sets
- pruning branches early to keep the search small
- restoring state cleanly on backtrack

Next file:
4) test_recursion_backtracking.py
"""

from __future__ import annotations

from typing import List, Sequence, Tuple


# ----------------------------
# N-Queens
# ----------------------------

def solve_n_queens(n: int) -> List[List[str]]:
    """
    Return all distinct solutions to the N-Queens puzzle.

    Each solution is a list of strings of length n:
      'Q' for queen, '.' for empty.

    Time: exponential; pruning makes it practical for small/medium n.
    """
    if n < 0:
        raise ValueError("n must be >= 0")
    if n == 0:
        return [[]]
    if n == 1:
        return [["Q"]]

    out: List[List[str]] = []
    cols = set()
    diag1 = set()  # r - c
    diag2 = set()  # r + c
    placement: List[int] = [-1] * n  # placement[r] = c

    def dfs(r: int) -> None:
        if r == n:
            out.append(_render_board(placement, n))
            return
        for c in range(n):
            d1 = r - c
            d2 = r + c
            if c in cols or d1 in diag1 or d2 in diag2:
                continue
            cols.add(c)
            diag1.add(d1)
            diag2.add(d2)
            placement[r] = c

            dfs(r + 1)

            placement[r] = -1
            cols.remove(c)
            diag1.remove(d1)
            diag2.remove(d2)

    dfs(0)
    return out


def _render_board(placement: List[int], n: int) -> List[str]:
    board: List[str] = []
    for r in range(n):
        c = placement[r]
        row = ["."]
        row *= n
        row[c] = "Q"
        board.append("".join(row))
    return board


# ----------------------------
# Balanced parentheses (pruned recursion)
# ----------------------------

def generate_parentheses(n: int) -> List[str]:
    """
    Generate all combinations of n pairs of balanced parentheses.

    Pruning:
      - never place ')' if it would exceed '(' count
      - stop when length == 2n

    Example:
      n=3 -> ["((()))","(()())","(())()","()(())","()()()"]
    """
    if n < 0:
        raise ValueError("n must be >= 0")
    out: List[str] = []
    path: List[str] = []

    def dfs(open_used: int, close_used: int) -> None:
        if open_used == n and close_used == n:
            out.append("".join(path))
            return
        if open_used < n:
            path.append("(")
            dfs(open_used + 1, close_used)
            path.pop()
        if close_used < open_used:
            path.append(")")
            dfs(open_used, close_used + 1)
            path.pop()

    dfs(0, 0)
    return out


# ----------------------------
# Word Search (grid DFS backtracking)
# ----------------------------

def word_exists(board: Sequence[Sequence[str]], word: str) -> bool:
    """
    Return True if word can be found in the grid by moving up/down/left/right
    without reusing the same cell.

    Early exits / pruning:
      - if word longer than #cells -> False
      - if board doesn't contain enough of a letter -> False (cheap frequency check)
      - stop DFS as soon as we match full word
    """
    if word == "":
        return True

    rows = len(board)
    if rows == 0:
        return False
    cols = len(board[0])
    if cols == 0:
        return False
    if any(len(row) != cols for row in board):
        raise ValueError("board must be rectangular")

    if len(word) > rows * cols:
        return False

    # Cheap frequency pruning
    freq = {}
    for r in range(rows):
        for c in range(cols):
            ch = board[r][c]
            freq[ch] = freq.get(ch, 0) + 1
    for ch in word:
        freq[ch] = freq.get(ch, 0) - 1
        if freq[ch] < 0:
            return False

    visited = [[False] * cols for _ in range(rows)]
    dirs: List[Tuple[int, int]] = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def dfs(r: int, c: int, i: int) -> bool:
        # i is index into word we need to match at (r,c)
        if board[r][c] != word[i]:
            return False
        if i == len(word) - 1:
            return True

        visited[r][c] = True
        nxt_i = i + 1
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                if dfs(nr, nc, nxt_i):
                    visited[r][c] = False
                    return True
        visited[r][c] = False
        return False

    # Start DFS from every cell that matches word[0]
    first = word[0]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == first:
                if dfs(r, c, 0):
                    return True
    return False


if __name__ == "__main__":
    print("N-Queens n=4 solutions:", len(solve_n_queens(4)))
    print("paren n=3:", generate_parentheses(3))

    grid = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"],
    ]
    print("word ABCCED:", word_exists(grid, "ABCCED"))
    print("word SEE:", word_exists(grid, "SEE"))
    print("word ABCB:", word_exists(grid, "ABCB"))
