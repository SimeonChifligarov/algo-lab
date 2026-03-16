"""
Shortest Paths — Bellman–Ford (negative weights + negative cycle detection) (Part 3/4)

Implements:
- bellman_ford: compute shortest distances from start, detect negative cycles
- bellman_ford_shortest_path: reconstruct path if no negative cycle affects goal
- extract_negative_cycle: if a negative cycle is reachable, return one such cycle

Bellman–Ford:
- Works with negative edges.
- Detects negative cycles reachable from the start.

Notes on "negative cycle detection":
If a negative cycle is reachable from start, shortest paths are undefined
for nodes reachable from that cycle.

Next file:
4) test_shortest_paths.py
"""

from __future__ import annotations

from typing import Dict, Hashable, List, Optional, Tuple, TypeVar

from weighted_graph import WeightedDiGraph

T = TypeVar("T", bound=Hashable)


def bellman_ford(
        g: WeightedDiGraph[T],
        start: T,
) -> Tuple[Dict[T, float], Dict[T, Optional[T]], Optional[List[T]]]:
    """
    Run Bellman–Ford from start.

    Returns:
      (dist, parent, neg_cycle)

    - dist: shortest distances to nodes (may be incomplete if unreachable)
    - parent: predecessor pointers for path reconstruction
    - neg_cycle: None if no reachable negative cycle, else a list of nodes
      representing one negative cycle (cycle order, ends where it starts)
    """
    if start not in g:
        raise KeyError(f"start node {start!r} not in graph")

    nodes = g.nodes()
    dist: Dict[T, float] = {u: float("inf") for u in nodes}
    parent: Dict[T, Optional[T]] = {u: None for u in nodes}
    dist[start] = 0.0

    edges = g.edges()

    # Relax edges up to |V|-1 times
    for _ in range(len(nodes) - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] == float("inf"):
                continue
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                changed = True
        if not changed:
            break

    # One more pass to detect negative cycles reachable from start
    x: Optional[T] = None
    for u, v, w in edges:
        if dist[u] == float("inf"):
            continue
        if dist[u] + w < dist[v]:
            parent[v] = u
            x = v
            break

    if x is None:
        # remove unreachable nodes (optional cleanliness)
        dist = {u: d for u, d in dist.items() if d != float("inf")}
        parent = {u: parent[u] for u in dist}
        return dist, parent, None

    cycle = extract_negative_cycle(parent, x)
    return dist, parent, cycle


def extract_negative_cycle(parent: Dict[T, Optional[T]], x: T) -> List[T]:
    """
    Given a parent map and a node x that was just relaxed in the |V|th iteration,
    reconstruct one negative cycle.

    Trick:
      - Walk parent pointers |V| times to ensure we're inside the cycle.
      - Then walk until we repeat a node.
    """
    # Step 1: move into the cycle
    # (we don't know |V| here; using len(parent) as an upper bound)
    y: Optional[T] = x
    for _ in range(len(parent)):
        y = parent.get(y)  # type: ignore[assignment]

    if y is None:
        # Shouldn't happen in normal BF cycle extraction, but guard anyway.
        return []

    # Step 2: collect cycle by walking until repetition
    cycle_nodes: List[T] = []
    cur: Optional[T] = y
    seen: Dict[T, int] = {}
    while cur is not None and cur not in seen:
        seen[cur] = len(cycle_nodes)
        cycle_nodes.append(cur)
        cur = parent.get(cur)

    if cur is None:
        return []

    # cur is the repeated node; slice from its first occurrence
    start_idx = seen[cur]
    cycle = cycle_nodes[start_idx:]
    cycle.append(cur)  # close the cycle
    cycle.reverse()  # optional: present in forward direction
    return cycle


def bellman_ford_shortest_path(g: WeightedDiGraph[T], start: T, goal: T) -> Optional[List[T]]:
    """
    Return a shortest path start->goal if well-defined, else:
    - None if goal unreachable
    - raises ValueError if a reachable negative cycle exists (paths not well-defined)

    For learning simplicity, we treat any reachable negative cycle as an error.
    """
    dist, parent, neg_cycle = bellman_ford(g, start)
    if neg_cycle is not None:
        raise ValueError(f"Negative cycle reachable from start: {neg_cycle}")
    if goal not in dist:
        return None
    return _reconstruct(parent, start, goal)


def _reconstruct(parent: Dict[T, Optional[T]], start: T, goal: T) -> List[T]:
    path: List[T] = []
    cur: Optional[T] = goal
    while cur is not None:
        path.append(cur)
        if cur == start:
            break
        cur = parent.get(cur)
    path.reverse()
    return path if path and path[0] == start else []


if __name__ == "__main__":
    g = WeightedDiGraph.from_edges([
        ("A", "B", 1),
        ("B", "C", 2),
        ("A", "C", 10),
        ("C", "D", -5),
        ("D", "B", 1),
    ])
    dist, parent, cycle = bellman_ford(g, "A")
    print("dist:", dist)
    print("cycle:", cycle)
