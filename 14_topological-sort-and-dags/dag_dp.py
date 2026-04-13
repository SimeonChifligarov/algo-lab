"""
Topological Sort & DAGs — DAG DP (longest path) (Part 3/4)

Implements:
- longest_path_dag: longest path length and one actual path (unweighted)
- longest_path_dag_weighted: longest path in a DAG with edge weights

Approach:
1) Compute topo order (must be a DAG).
2) DP over topo order:
     dp[v] = best distance to v
     parent[v] = predecessor on best path
3) Track best endpoint and reconstruct path.

Notes:
- For unweighted graphs, each edge has weight 1.
- For weighted, edge weights can be int/float.

Next file:
4) test_topo_and_dag.py
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Hashable, List, Optional, Tuple, TypeVar

try:
    from .dag_core import DiGraph
except ImportError:
    from dag_core import DiGraph
try:
    from .topo_sort import topo_kahn
except ImportError:
    from topo_sort import topo_kahn

T = TypeVar("T", bound=Hashable)


def longest_path_dag(g: DiGraph[T]) -> Tuple[int, List[T]]:
    """
    Return (length, path) of the longest path in a DAG.
    Length is number of edges in the path.
    For empty graph, returns (0, []).

    If graph is not a DAG, raises ValueError.
    """
    if len(g) == 0:
        return 0, []

    order = topo_kahn(g)
    dp: Dict[T, int] = {u: 0 for u in order}
    parent: Dict[T, Optional[T]] = {u: None for u in order}

    best_end = order[0]
    best_len = 0

    for u in order:
        if dp[u] > best_len:
            best_len = dp[u]
            best_end = u
        for v in g.neighbors(u):
            cand = dp[u] + 1
            if cand > dp.get(v, 0):
                dp[v] = cand
                parent[v] = u

    # find best endpoint (in case it was updated via neighbors not in dp init)
    for v, d in dp.items():
        if d > best_len:
            best_len = d
            best_end = v

    path = _reconstruct_path(parent, best_end)
    return best_len, path


def _reconstruct_path(parent: Dict[T, Optional[T]], end: T) -> List[T]:
    path: List[T] = []
    cur: Optional[T] = end
    while cur is not None:
        path.append(cur)
        cur = parent.get(cur)
    path.reverse()
    return path


# ----------------------------
# Weighted version
# ----------------------------

def longest_path_dag_weighted(
        g: DiGraph[T],
        weights: Dict[Tuple[T, T], float],
) -> Tuple[float, List[T]]:
    """
    Return (max_weight, path) for longest path in a DAG given edge weights.

    weights[(u,v)] gives weight for edge u->v. Missing edges default to 0.0.

    If graph is empty: returns (0.0, [])
    If graph not a DAG: raises ValueError
    """
    if len(g) == 0:
        return 0.0, []

    order = topo_kahn(g)
    dp: Dict[T, float] = {u: 0.0 for u in order}
    parent: Dict[T, Optional[T]] = {u: None for u in order}

    best_end = order[0]
    best_val = 0.0

    for u in order:
        if dp[u] > best_val:
            best_val = dp[u]
            best_end = u
        for v in g.neighbors(u):
            w = weights.get((u, v), 0.0)
            cand = dp[u] + w
            if cand > dp.get(v, 0.0):
                dp[v] = cand
                parent[v] = u

    for v, d in dp.items():
        if d > best_val:
            best_val = d
            best_end = v

    path = _reconstruct_path(parent, best_end)
    return best_val, path


if __name__ == "__main__":
    g = DiGraph.from_edges([("A", "B"), ("B", "C"), ("A", "C"), ("C", "D")])
    print("longest unweighted:", longest_path_dag(g))  # 3 edges path A->B->C->D

    w = {("A", "B"): 2.0, ("B", "C"): 3.0, ("A", "C"): 10.0, ("C", "D"): 1.0}
    print("longest weighted:", longest_path_dag_weighted(g, w))
