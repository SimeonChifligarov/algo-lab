"""
Shortest Paths — Dijkstra (non-negative weights) (Part 2/4)

Implements:
- dijkstra_distances: shortest distances from start to all reachable nodes
- dijkstra_shortest_path: reconstruct one shortest path start->goal
- dijkstra_parents: parent pointers produced by Dijkstra

Requirements:
- All edge weights must be non-negative.

Approach:
- Use a min-priority queue (heapq) of (dist, node)
- Classic "lazy" decrease-key: push new (better) entries; ignore stale ones
- Maintain parent pointers for reconstruction

Next file:
3) bellman_ford.py
"""

from __future__ import annotations

import heapq
from typing import Dict, Hashable, List, Optional, Tuple, TypeVar

try:
    from .weighted_graph import WeightedDiGraph
except ImportError:
    from weighted_graph import WeightedDiGraph
T = TypeVar("T", bound=Hashable)


def dijkstra_parents(g: WeightedDiGraph[T], start: T) -> Tuple[Dict[T, float], Dict[T, Optional[T]]]:
    """
    Run Dijkstra from start.
    Returns (dist, parent), where:
      - dist[u] is shortest distance from start to u
      - parent[u] is previous node on a shortest path (parent[start] = None)
    """
    if start not in g:
        raise KeyError(f"start node {start!r} not in graph")

    g.validate_no_negative_weights()

    dist: Dict[T, float] = {start: 0.0}
    parent: Dict[T, Optional[T]] = {start: None}

    heap: List[Tuple[float, T]] = [(0.0, start)]

    while heap:
        d, u = heapq.heappop(heap)
        # stale entry?
        if d != dist.get(u, float("inf")):
            continue

        for v, w in g.neighbors(u):
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                parent[v] = u
                heapq.heappush(heap, (nd, v))

    return dist, parent


def dijkstra_distances(g: WeightedDiGraph[T], start: T) -> Dict[T, float]:
    """Convenience wrapper returning only dist."""
    dist, _ = dijkstra_parents(g, start)
    return dist


def dijkstra_shortest_path(g: WeightedDiGraph[T], start: T, goal: T) -> Optional[List[T]]:
    """
    Return one shortest path from start to goal (inclusive), or None if unreachable.
    """
    dist, parent = dijkstra_parents(g, start)
    if goal not in dist:
        return None
    return _reconstruct(parent, goal)


def _reconstruct(parent: Dict[T, Optional[T]], goal: T) -> List[T]:
    path: List[T] = []
    cur: Optional[T] = goal
    while cur is not None:
        path.append(cur)
        cur = parent.get(cur)
    path.reverse()
    return path


if __name__ == "__main__":
    g = WeightedDiGraph.from_edges([
        ("A", "B", 1),
        ("B", "C", 2),
        ("A", "C", 10),
        ("C", "D", 1),
        ("B", "D", 10),
    ])
    print("dist:", dijkstra_distances(g, "A"))
    print("path A->D:", dijkstra_shortest_path(g, "A", "D"))
