"""
Stacks & Queues — queue fundamentals + queue-backed patterns (Part 3/4)

This file covers:
- Queue (FIFO) wrapper using collections.deque
- CircularQueue (fixed-capacity ring buffer, educational)
- MovingAverage (streaming fixed-size window)
- RecentCounter (count events in the last N time units)
- bfs_shortest_path_grid (classic queue-backed BFS)

Next file:
4) test_stacks_queues.py
"""

from __future__ import annotations

from collections import deque
from typing import Deque, Generic, Iterable, Iterator, List, Optional, Sequence, Tuple, TypeVar

T = TypeVar("T")


# ----------------------------
# Basic queue (deque-backed)
# ----------------------------

class Queue(Generic[T]):
    """
    Minimal FIFO queue wrapper (backed by collections.deque).

    Operations:
      enqueue, dequeue, peek, is_empty, len, iter
    """

    def __init__(self, items: Optional[Iterable[T]] = None):
        self._dq: Deque[T] = deque()
        if items is not None:
            for x in items:
                self._dq.append(x)

    def enqueue(self, x: T) -> None:
        self._dq.append(x)

    def dequeue(self) -> T:
        if not self._dq:
            raise IndexError("dequeue from empty queue")
        return self._dq.popleft()

    def peek(self) -> T:
        if not self._dq:
            raise IndexError("peek from empty queue")
        return self._dq[0]

    def is_empty(self) -> bool:
        return not self._dq

    def __len__(self) -> int:
        return len(self._dq)

    def __iter__(self) -> Iterator[T]:
        return iter(self._dq)

    def __repr__(self) -> str:
        return f"Queue({list(self._dq)!r})"


# ----------------------------
# Circular queue (ring buffer, fixed capacity)
# ----------------------------

class CircularQueue(Generic[T]):
    """
    Fixed-capacity queue implemented with a ring buffer.

    Good for understanding queue internals:
    - O(1) enqueue/dequeue
    - head/tail wrap around using modulo

    Raises:
      OverflowError on enqueue when full
      IndexError on dequeue/peek when empty
    """

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity must be > 0")
        self._buf: List[Optional[T]] = [None] * capacity
        self._cap = capacity
        self._head = 0
        self._tail = 0
        self._size = 0

    @property
    def capacity(self) -> int:
        return self._cap

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def is_full(self) -> bool:
        return self._size == self._cap

    def enqueue(self, x: T) -> None:
        if self.is_full():
            raise OverflowError("enqueue to full CircularQueue")
        self._buf[self._tail] = x
        self._tail = (self._tail + 1) % self._cap
        self._size += 1

    def dequeue(self) -> T:
        if self.is_empty():
            raise IndexError("dequeue from empty CircularQueue")
        x = self._buf[self._head]
        self._buf[self._head] = None
        self._head = (self._head + 1) % self._cap
        self._size -= 1
        return x  # type: ignore[return-value]

    def peek(self) -> T:
        if self.is_empty():
            raise IndexError("peek from empty CircularQueue")
        return self._buf[self._head]  # type: ignore[return-value]

    def __iter__(self) -> Iterator[T]:
        for i in range(self._size):
            idx = (self._head + i) % self._cap
            yield self._buf[idx]  # type: ignore[misc]

    def __repr__(self) -> str:
        return f"CircularQueue(capacity={self._cap}, items={list(self)!r})"


# ----------------------------
# Queue-backed stream patterns
# ----------------------------

class MovingAverage:
    """
    Streaming moving average over the last `window_size` values.

    Example:
      ma = MovingAverage(3)
      ma.next(1) -> 1.0
      ma.next(10) -> 5.5
      ma.next(3) -> 14/3
      ma.next(5) -> 6.0    (window is now [10,3,5])
    """

    def __init__(self, window_size: int):
        if window_size <= 0:
            raise ValueError("window_size must be > 0")
        self._k = window_size
        self._q: Deque[float] = deque()
        self._sum = 0.0

    def next(self, value: float) -> float:
        self._q.append(float(value))
        self._sum += float(value)

        if len(self._q) > self._k:
            self._sum -= self._q.popleft()

        return self._sum / len(self._q)

    def __len__(self) -> int:
        return len(self._q)


class RecentCounter:
    """
    Count events in a sliding time window using a queue.

    `ping(t)` records an event at time t and returns the number of events
    in [t - window + 1, t].

    Assumes calls come in non-decreasing time order.

    Default window=3000 matches the classic interview problem.
    """

    def __init__(self, window: int = 3000):
        if window <= 0:
            raise ValueError("window must be > 0")
        self._window = window
        self._q: Deque[int] = deque()

    def ping(self, t: int) -> int:
        self._q.append(t)
        left = t - self._window + 1
        while self._q and self._q[0] < left:
            self._q.popleft()
        return len(self._q)

    def __len__(self) -> int:
        return len(self._q)


# ----------------------------
# BFS pattern (queue-backed)
# ----------------------------

Grid = Sequence[Sequence[int]]
Cell = Tuple[int, int]


def bfs_shortest_path_grid(grid: Grid, start: Cell, goal: Cell) -> int:
    """
    Return shortest path length in a 4-direction grid using BFS.

    Conventions:
    - grid[r][c] == 0  -> open cell
    - grid[r][c] == 1  -> blocked cell
    - movement allowed up/down/left/right
    - returns number of steps from start to goal
    - returns -1 if unreachable

    Edge cases:
    - invalid coordinates -> ValueError
    - blocked start/goal -> -1
    """
    rows = len(grid)
    if rows == 0:
        return -1
    cols = len(grid[0])
    if cols == 0:
        return -1
    if any(len(row) != cols for row in grid):
        raise ValueError("grid must be rectangular")

    sr, sc = start
    gr, gc = goal

    def in_bounds(r: int, c: int) -> bool:
        return 0 <= r < rows and 0 <= c < cols

    if not in_bounds(sr, sc) or not in_bounds(gr, gc):
        raise ValueError("start/goal out of bounds")
    if grid[sr][sc] != 0 or grid[gr][gc] != 0:
        return -1
    if start == goal:
        return 0

    q: Deque[Tuple[int, int, int]] = deque()  # (r, c, dist)
    q.append((sr, sc, 0))
    seen = {(sr, sc)}

    for_dr_dc = ((1, 0), (-1, 0), (0, 1), (0, -1))

    while q:
        r, c, d = q.popleft()
        for dr, dc in for_dr_dc:
            nr, nc = r + dr, c + dc
            if not in_bounds(nr, nc):
                continue
            if grid[nr][nc] != 0:
                continue
            if (nr, nc) in seen:
                continue
            if (nr, nc) == (gr, gc):
                return d + 1
            seen.add((nr, nc))
            q.append((nr, nc, d + 1))

    return -1


if __name__ == "__main__":
    q = Queue([1, 2, 3])
    q.enqueue(4)
    print("queue:", q, "peek:", q.peek(), "dequeue:", q.dequeue(), "now:", q)

    cq = CircularQueue(3)
    cq.enqueue(10)
    cq.enqueue(20)
    print("circular:", cq)
    print("dequeue:", cq.dequeue())
    cq.enqueue(30)
    cq.enqueue(40)
    print("circular wrap:", cq)

    ma = MovingAverage(3)
    for x in [1, 10, 3, 5]:
        print("moving avg next", x, "->", ma.next(x))

    rc = RecentCounter()
    for t in [1, 100, 3001, 3002]:
        print("ping", t, "->", rc.ping(t))

    grid = [
        [0, 0, 1, 0],
        [1, 0, 1, 0],
        [0, 0, 0, 0],
    ]
    print("bfs shortest path:", bfs_shortest_path_grid(grid, (0, 0), (2, 3)))
