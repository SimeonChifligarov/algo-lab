"""
Shortest Paths — weighted directed graph core (Part 1/4)

This module defines a simple weighted directed graph representation:
- WeightedDiGraph: adjacency list mapping u -> list of (v, w)
- add_edge, add_node
- nodes(), edges()
- validate_no_negative_weights (useful for Dijkstra)

Next files:
2) dijkstra.py
3) bellman_ford.py
4) test_shortest_paths.py

Design:
- Nodes can be any hashable type.
- Graph is directed by default (shortest paths are usually taught that way),
  but you can model undirected graphs by adding edges both ways.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Generic, Hashable, Iterable, List, Optional, Tuple, TypeVar

T = TypeVar("T", bound=Hashable)


@dataclass
class WeightedDiGraph(Generic[T]):
    _adj: Dict[T, List[Tuple[T, float]]] = field(default_factory=dict)

    def add_node(self, u: T) -> None:
        if u not in self._adj:
            self._adj[u] = []

    def add_edge(self, u: T, v: T, w: float) -> None:
        """
        Add directed edge u -> v with weight w.
        Automatically adds missing nodes.
        """
        self.add_node(u)
        self.add_node(v)
        self._adj[u].append((v, float(w)))

    def neighbors(self, u: T) -> List[Tuple[T, float]]:
        """Return outgoing neighbors (v, w)."""
        return list(self._adj.get(u, []))

    def nodes(self) -> List[T]:
        return list(self._adj.keys())

    def edges(self) -> List[Tuple[T, T, float]]:
        out: List[Tuple[T, T, float]] = []
        for u, ns in self._adj.items():
            for v, w in ns:
                out.append((u, v, w))
        return out

    def __contains__(self, u: T) -> bool:
        return u in self._adj

    def __len__(self) -> int:
        return len(self._adj)

    def __repr__(self) -> str:
        m = sum(len(ns) for ns in self._adj.values())
        return f"WeightedDiGraph(n={len(self._adj)}, m={m})"

    @classmethod
    def from_edges(cls, edges: Iterable[Tuple[T, T, float]]) -> "WeightedDiGraph[T]":
        g = cls()
        for u, v, w in edges:
            g.add_edge(u, v, w)
        return g

    def validate_no_negative_weights(self) -> None:
        """
        Raise ValueError if any edge weight is negative.
        Dijkstra requires non-negative weights.
        """
        for u, v, w in self.edges():
            if w < 0:
                raise ValueError(f"Negative edge weight found: {u!r}->{v!r} weight={w}")


if __name__ == "__main__":
    g = WeightedDiGraph.from_edges([("A", "B", 1), ("B", "C", 2), ("A", "C", 10)])
    print(g)
    print("edges:", g.edges())
