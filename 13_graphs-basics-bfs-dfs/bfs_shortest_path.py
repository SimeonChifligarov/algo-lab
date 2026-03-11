"""
Graphs Basics (BFS/DFS) — BFS shortest paths + path reconstruction (Part 2/4)

This file implements BFS for unweighted graphs:
- bfs_distances: distance from start to all reachable nodes
- bfs_shortest_path: reconstruct one shortest path from start to goal
- bfs_parents: parent pointers (for later reconstruction / tree view)

Key idea:
BFS explores in "layers", so the first time you reach a node is via a shortest path.

Next files:
3) dfs_algorithms.py
4) test_graphs.py
"""

from __future__ import annotations

from collections import deque
from typing import Deque, Dict, Generic, Hashable, List, Optional, Sequence, Tuple, TypeVar

from graph_core import Graph

T = TypeVar("T", bound=Hashable)


def bfs_parents(g: Graph[T], start: T) -> Dict[T, Optional[T]]:
    """
    Return parent pointers from BFS rooted at start.

    parent[start] = None
    For any visited node v != start, parent[v] is the node we came from first.
    """
    if start not in g:
        raise KeyError(f"start node {start!r} not in graph")

    q: Deque[T] = deque([start])
    parent: Dict[T, Optional[T]] = {start: None}

    while q:
        u = q.popleft()
        for v in g.neighbors(u):
            if v not in parent:
                parent[v] = u
                q.append(v)

    return parent


def bfs_distances(g: Graph[T], start: T) -> Dict[T, int]:
    """
    Return shortest-path distances from start to all reachable nodes.
    """
    parent = bfs_parents(g, start)
    dist: Dict[T, int] = {}
    for node in parent:
        # compute dist by walking parents (fine for learning; could be done inline in BFS too)
        d = 0
        cur = node
        while cur is not None and cur != start:
            cur = parent[cur]
            d += 1
        dist[node] = d
    return dist


def bfs_shortest_path(g: Graph[T], start: T, goal: T) -> Optional[List[T]]:
    """
    Return one shortest path from start to goal (inclusive), or None if unreachable.

    Uses BFS parent pointers then reconstructs by walking backwards from goal.
    """
    parent = bfs_parents(g, start)
    if goal not in parent:
        return None

    path: List[T] = []
    cur: Optional[T] = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path


if __name__ == "__main__":
    g = Graph.from_edges(
        [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")],
        directed=False,
    )
    print("dist:", bfs_distances(g, "A"))
    print("path A->E:", bfs_shortest_path(g, "A", "E"))
