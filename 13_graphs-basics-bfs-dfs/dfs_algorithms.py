"""
Graphs Basics (BFS/DFS) — DFS patterns (Part 3/4)

This file implements:
- dfs_reachable: reachability set from a start node
- connected_components (undirected): list of components as sets
- has_cycle_undirected: cycle detection in undirected graphs
- has_cycle_directed: cycle detection in directed graphs (color/recursion stack)

These are core DFS ideas:
- mark visited to avoid infinite loops
- parent tracking for undirected cycle detection
- recursion-stack (gray set) for directed cycle detection

Next file:
4) test_graphs.py
"""

from __future__ import annotations

from typing import Dict, Hashable, List, Optional, Set, TypeVar

from graph_core import Graph

T = TypeVar("T", bound=Hashable)


def dfs_reachable(g: Graph[T], start: T) -> Set[T]:
    """
    Return the set of nodes reachable from start using DFS (iterative).
    """
    if start not in g:
        raise KeyError(f"start node {start!r} not in graph")

    seen: Set[T] = set()
    stack: List[T] = [start]
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        for v in g.neighbors(u):
            if v not in seen:
                stack.append(v)
    return seen


def connected_components(g: Graph[T]) -> List[Set[T]]:
    """
    Return connected components of an UNDIRECTED graph as a list of sets.

    Raises ValueError if g is directed.
    """
    if g.directed:
        raise ValueError("connected_components requires an undirected graph")

    comps: List[Set[T]] = []
    seen: Set[T] = set()

    for u in g.nodes():
        if u in seen:
            continue
        comp = dfs_reachable(g, u)
        comps.append(comp)
        seen |= comp

    return comps


def has_cycle_undirected(g: Graph[T]) -> bool:
    """
    Detect cycle in an UNDIRECTED graph using DFS + parent.

    Raises ValueError if g is directed.
    """
    if g.directed:
        raise ValueError("has_cycle_undirected requires an undirected graph")

    seen: Set[T] = set()

    for start in g.nodes():
        if start in seen:
            continue

        stack: List[tuple[T, Optional[T]]] = [(start, None)]  # (node, parent)
        while stack:
            u, parent = stack.pop()
            if u in seen:
                continue
            seen.add(u)

            for v in g.neighbors(u):
                if v == parent:
                    continue
                if v in seen:
                    return True
                stack.append((v, u))

    return False


def has_cycle_directed(g: Graph[T]) -> bool:
    """
    Detect cycle in a DIRECTED graph using DFS recursion stack ("colors").

    Colors:
      0 = unvisited
      1 = visiting (in recursion stack)
      2 = done

    Raises ValueError if g is undirected.
    """
    if not g.directed:
        raise ValueError("has_cycle_directed requires a directed graph")

    color: Dict[T, int] = {u: 0 for u in g.nodes()}

    def dfs(u: T) -> bool:
        color[u] = 1
        for v in g.neighbors(u):
            if v not in color:
                color[v] = 0
            if color[v] == 1:
                return True
            if color[v] == 0 and dfs(v):
                return True
        color[u] = 2
        return False

    for u in list(color.keys()):
        if color[u] == 0:
            if dfs(u):
                return True
    return False


if __name__ == "__main__":
    ug = Graph.from_edges([(1, 2), (2, 3), (3, 1)], directed=False)
    print("reachable from 1:", dfs_reachable(ug, 1))
    print("components:", connected_components(ug))
    print("cycle undirected:", has_cycle_undirected(ug))

    dg = Graph.from_edges([(1, 2), (2, 3), (3, 1)], directed=True)
    print("cycle directed:", has_cycle_directed(dg))
