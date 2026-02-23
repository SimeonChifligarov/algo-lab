"""
Stacks & Queues — stack fundamentals (Part 1/4)

This first file gives you the stack primitives and classic "stack parsing" patterns:
- Stack class (thin wrapper over list) with clear API
- Valid parentheses / bracket matching
- Simplified path normalization (like Unix paths)
- Evaluate Reverse Polish Notation (RPN)

Next files:
2) monotonic_stack.py   (next greater element, daily temps, histogram)
3) queue_basics.py      (Queue/Deque, BFS-style pattern, moving average)
4) test_stacks_queues.py (unittest suite)

All standard-library-only.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterable, Iterator, List, Optional, TypeVar

T = TypeVar("T")


class Stack(Generic[T]):
    """
    Minimal stack wrapper.

    Operations:
      push, pop, peek, is_empty, len, iter
    """

    def __init__(self, items: Optional[Iterable[T]] = None):
        self._data: List[T] = []
        if items is not None:
            for x in items:
                self._data.append(x)

    def push(self, x: T) -> None:
        self._data.append(x)

    def pop(self) -> T:
        if not self._data:
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self) -> T:
        if not self._data:
            raise IndexError("peek from empty stack")
        return self._data[-1]

    def is_empty(self) -> bool:
        return not self._data

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[T]:
        # iterate from bottom to top
        return iter(self._data)

    def __repr__(self) -> str:
        return f"Stack({self._data!r})"


# ----------------------------
# Parsing / validation patterns
# ----------------------------

def is_valid_brackets(s: str) -> bool:
    """
    Return True if brackets in s are balanced and properly nested.

    Supports (), [], {}.
    Ignores non-bracket characters.

    Examples:
      "([])" -> True
      "([)]" -> False
    """
    pairs = {")": "(", "]": "[", "}": "{"}
    opens = set(pairs.values())
    st: List[str] = []

    for ch in s:
        if ch in opens:
            st.append(ch)
        elif ch in pairs:
            if not st or st[-1] != pairs[ch]:
                return False
            st.pop()

    return not st


def simplify_path(path: str) -> str:
    """
    Simplify a Unix-style path.

    Rules:
    - multiple slashes collapse into one
    - '.' means current dir (ignore)
    - '..' pops one dir if possible
    - path is treated as absolute if it starts with '/', else relative

    Examples:
      "/a/./b/../../c/" -> "/c"
      "a/b/../c" -> "a/c"
    """
    if path == "":
        return "."

    is_abs = path.startswith("/")
    parts = [p for p in path.split("/") if p != ""]
    st: List[str] = []

    for p in parts:
        if p == ".":
            continue
        if p == "..":
            if st and (is_abs or st[-1] != ".."):
                st.pop()
            else:
                if not is_abs:
                    st.append("..")
        else:
            st.append(p)

    if is_abs:
        return "/" + "/".join(st)
    return "/".join(st) if st else "."


# ----------------------------
# Expression evaluation (RPN)
# ----------------------------

def eval_rpn(tokens: List[str]) -> int:
    """
    Evaluate an expression in Reverse Polish Notation.

    Supported operators: +, -, *, /
    Division truncates toward zero (like LeetCode's version).

    Example:
      ["2","1","+","3","*"] -> 9
    """
    st: List[int] = []

    def pop2() -> tuple[int, int]:
        if len(st) < 2:
            raise ValueError("Invalid RPN: not enough operands")
        b = st.pop()
        a = st.pop()
        return a, b

    for t in tokens:
        if t in {"+", "-", "*", "/"}:
            a, b = pop2()
            if t == "+":
                st.append(a + b)
            elif t == "-":
                st.append(a - b)
            elif t == "*":
                st.append(a * b)
            else:
                if b == 0:
                    raise ZeroDivisionError("division by zero in RPN")
                st.append(int(a / b))  # truncates toward 0
        else:
            try:
                st.append(int(t))
            except ValueError as e:
                raise ValueError(f"Invalid token: {t!r}") from e

    if len(st) != 1:
        raise ValueError("Invalid RPN: leftover operands/operators")
    return st[0]


if __name__ == "__main__":
    print("valid brackets:", is_valid_brackets("([]){}"))
    print("simplify:", simplify_path("/a/./b/../../c/"))
    print("rpn:", eval_rpn(["2", "1", "+", "3", "*"]))
