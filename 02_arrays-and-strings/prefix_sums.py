"""
Prefix sums + range sum queries.

This file gives you a small reusable object, PrefixSum, that:
- Builds prefix sums from an iterable of numbers
- Answers sum over [l, r) in O(1)
- Handles edge cases (empty input, bounds checking)
- Optionally supports updating via Fenwick tree (Binary Indexed Tree)

Why two structures?
- Plain prefix sums: fastest queries, but updates require rebuild.
- Fenwick tree: supports point updates in O(log n) and range sums in O(log n).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence, Union

Number = Union[int, float]


def _validate_bounds(n: int, l: int, r: int) -> None:
    if l < 0 or r < 0:
        raise IndexError("Indices must be non-negative")
    if l > r:
        raise IndexError(f"Invalid range: l ({l}) > r ({r})")
    if r > n:
        raise IndexError(f"Range end r ({r}) out of bounds for length {n}")


@dataclass(frozen=True)
class PrefixSum:
    """
    Immutable prefix sums for fast range queries.

    Internals:
      prefix[i] = sum(data[:i]) for i in [0..n]
    So range_sum(l, r) = prefix[r] - prefix[l]
    """
    prefix: List[Number]

    @classmethod
    def from_iterable(cls, data: Iterable[Number]) -> "PrefixSum":
        prefix: List[Number] = [0]
        s: Number = 0
        for x in data:
            s = s + x
            prefix.append(s)
        return cls(prefix=prefix)

    @property
    def n(self) -> int:
        return len(self.prefix) - 1

    def total(self) -> Number:
        return self.prefix[-1]

    def range_sum(self, l: int, r: int) -> Number:
        _validate_bounds(self.n, l, r)
        return self.prefix[r] - self.prefix[l]


class FenwickSum:
    """
    Fenwick Tree (Binary Indexed Tree) for point updates + prefix/range sums.

    Methods:
      - prefix_sum(i): sum over [0, i)  (i is exclusive)
      - range_sum(l, r): sum over [l, r)
      - add(i, delta): data[i] += delta
      - set(i, value): data[i] = value

    Notes:
      Uses 1-based internal indexing.
    """

    def __init__(self, data: Sequence[Number]):
        self._n = len(data)
        self._tree: List[Number] = [0] * (self._n + 1)

        # IMPORTANT: start from zeros, then build using add().
        # If we started with list(data) and called add(i, x), we'd double-count in _data.
        self._data: List[Number] = [0] * self._n
        for i, x in enumerate(data):
            self.add(i, x)

    @property
    def n(self) -> int:
        return self._n

    def add(self, i: int, delta: Number) -> None:
        if i < 0 or i >= self._n:
            raise IndexError(f"Index {i} out of bounds for length {self._n}")
        idx = i + 1
        while idx <= self._n:
            self._tree[idx] = self._tree[idx] + delta
            idx += idx & -idx
        self._data[i] = self._data[i] + delta

    def set(self, i: int, value: Number) -> None:
        if i < 0 or i >= self._n:
            raise IndexError(f"Index {i} out of bounds for length {self._n}")
        delta = value - self._data[i]
        self.add(i, delta)

    def prefix_sum(self, i: int) -> Number:
        """
        Sum over [0, i), i exclusive.
        """
        if i < 0:
            raise IndexError("Index must be non-negative")
        if i > self._n:
            raise IndexError(f"Index {i} out of bounds for length {self._n}")

        res: Number = 0
        idx = i
        while idx > 0:
            res = res + self._tree[idx]
            idx -= idx & -idx
        return res

    def range_sum(self, l: int, r: int) -> Number:
        _validate_bounds(self._n, l, r)
        return self.prefix_sum(r) - self.prefix_sum(l)


if __name__ == "__main__":
    data = [3, -1, 4, 1, 5, 9]
    ps = PrefixSum.from_iterable(data)
    print("PrefixSum total:", ps.total())
    print("sum[1:4] =", ps.range_sum(1, 4))

    fw = FenwickSum(data)
    print("Fenwick sum[1:4] =", fw.range_sum(1, 4))
    fw.add(2, 10)
    print("after add, sum[1:4] =", fw.range_sum(1, 4))
    fw.set(1, 7)
    print("after set, sum[0:2] =", fw.range_sum(0, 2))
