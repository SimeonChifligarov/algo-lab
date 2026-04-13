"""
Topological Sort & DAGs — topological sorting + cycle detection (Part 2/4)

Implements:
- topo_kahn: Kahn’s algorithm (BFS on indegrees)
- topo_dfs: DFS postorder topological sort
- is_dag: cycle detection (directed)
- find_cycle: return one directed cycle as a list of nodes (if any)

Notes:
- A topological order exists iff the graph is a DAG (no directed cycles).
- For reproducibility, Kahn's algorithm can optionally use a heap to pick the
  smallest-available node first (when nodes are comparable).

Next file:
3) dag_dp.py
"""

from __future__ import annotations

from collections import deque
import heapq
from typing import Deque, Dict, Hashable, List, Optional, Set, Tuple, TypeVar

try:
    from .dag_core import DiGraph
except ImportError:
    from dag_core import DiGraph

T = TypeVar("T", bound=Hashable)


def topo_kahn(g: DiGraph[T], *, lexicographic: bool = False) -> List[T]:
    """
    Topological sort using Kahn's algorithm.

    If the graph contains a cycle, raises ValueError.

    If lexicographic=True, uses a min-heap so the output is the smallest-available
    node at each step (requires nodes be comparable).
    """
    indeg = g.indegrees()
    order: List[T] = []

    if lexicographic:
        heap: List[T] = [u for u, d in indeg.items() if d == 0]
        heapq.heapify(heap)
        pop_ready = lambda: heapq.heappop(heap)
        push_ready = lambda x: heapq.heappush(heap, x)
        ready_empty = lambda: len(heap) == 0
    else:
        q: Deque[T] = deque([u for u, d in indeg.items() if d == 0])
        pop_ready = lambda: q.popleft()
        push_ready = lambda x: q.append(x)
        ready_empty = lambda: len(q) == 0

    processed = 0
    while not ready_empty():
        u = pop_ready()
        order.append(u)
        processed += 1
        for v in g.neighbors(u):
            indeg[v] -= 1
            if indeg[v] == 0:
                push_ready(v)

    if processed != len(indeg):
        cycle = find_cycle(g)
        raise ValueError(f"Graph is not a DAG (cycle detected: {cycle})")
    return order


def topo_dfs(g: DiGraph[T]) -> List[T]:
    """
    Topological sort using DFS postorder.

    If a cycle is detected, raises ValueError.
    """
    color: Dict[T, int] = {u: 0 for u in g.nodes()}  # 0=unvisited,1=visiting,2=done
    post: List[T] = []

    def dfs(u: T) -> None:
        color[u] = 1
        for v in g.neighbors(u):
            if v not in color:
                color[v] = 0
            if color[v] == 1:
                cycle = find_cycle(g)
                raise ValueError(f"Graph is not a DAG (cycle detected: {cycle})")
            if color[v] == 0:
                dfs(v)
        color[u] = 2
        post.append(u)

    for u in list(color.keys()):
        if color[u] == 0:
            dfs(u)

    post.reverse()
    return post


def is_dag(g: DiGraph[T]) -> bool:
    """Return True if g has no directed cycle."""
    try:
        topo_kahn(g)
        return True
    except ValueError:
        return False


def find_cycle(g: DiGraph[T]) -> List[T]:
    """
    Return one directed cycle as a list of nodes in cycle order, e.g. [A,B,C,A].
    If no cycle exists, returns [].

    Uses DFS with parent pointers + recursion stack.
    """
    color: Dict[T, int] = {u: 0 for u in g.nodes()}  # 0,1,2
    parent: Dict[T, Optional[T]] = {u: None for u in g.nodes()}
    stack_set: Set[T] = set()

    cycle: List[T] = []

    def build_cycle(start: T, end: T) -> List[T]:
        # We found an edge start -> end where end is in recursion stack.
        # Reconstruct path from start back to end using parent pointers.
        path = [start]
        cur = start
        while cur != end and parent[cur] is not None:
            cur = parent[cur]  # type: ignore[assignment]
            path.append(cur)
        path.reverse()
        path.append(end)
        return path

    def dfs(u: T) -> bool:
        color[u] = 1
        stack_set.add(u)
        for v in g.neighbors(u):
            if v not in color:
                color[v] = 0
                parent[v] = None
            if color[v] == 0:
                parent[v] = u
                if dfs(v):
                    return True
            elif color[v] == 1:
                nonlocal cycle
                # found back edge u -> v
                cycle = build_cycle(u, v)
                return True
        color[u] = 2
        stack_set.discard(u)
        return False

    for u in g.nodes():
        if color.get(u, 0) == 0:
            if dfs(u):
                return cycle
    return []


if __name__ == "__main__":
    g = DiGraph.from_edges([("A", "C"), ("B", "C"), ("C", "D")])
    print("kahn:", topo_kahn(g, lexicographic=True))
    print("dfs:", topo_dfs(g))

    cyc = DiGraph.from_edges([(1, 2), (2, 3), (3, 1)])
    print("is_dag:", is_dag(cyc))
    print("cycle:", find_cycle(cyc))
