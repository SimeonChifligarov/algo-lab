"""
Graphs Basics (BFS/DFS) — core graph representation (Part 1/4)

This file defines a small, clean adjacency-list graph with utilities:
- Graph: directed or undirected
- add_edge, add_node
- neighbors
- from_edges constructor
- validation helpers

Next files:
2) bfs_shortest_path.py   (BFS distances + path reconstruction)
3) dfs_algorithms.py      (reachability, connected components, cycle detection)
4) test_graphs.py         (unittest suite)

Design:
- Nodes can be any hashable type (int, str, tuple, ...)
- The adjacency list stores sets to avoid duplicate edges.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Generic, Hashable, Iterable, Iterator, List, Optional, Set, Tuple, TypeVar

T = TypeVar("T", bound=Hashable)


@dataclass
class Graph(Generic[T]):
    directed: bool = False
    _adj: Dict[T, Set[T]] = field(default_factory=dict)

    def add_node(self, u: T) -> None:
        """Ensure node u exists in the adjacency list."""
        if u not in self._adj:
            self._adj[u] = set()

    def add_edge(self, u: T, v: T) -> None:
        """
        Add an edge u->v (and v->u if undirected).
        Automatically adds missing nodes.
        """
        self.add_node(u)
        self.add_node(v)
        self._adj[u].add(v)
        if not self.directed:
            self._adj[v].add(u)

    def neighbors(self, u: T) -> Set[T]:
        """Return neighbor set for u (empty set if u is unknown)."""
        return self._adj.get(u, set())

    def nodes(self) -> List[T]:
        """Return list of nodes (arbitrary order)."""
        return list(self._adj.keys())

    def edges(self) -> List[Tuple[T, T]]:
        """Return list of edges (u, v). For undirected, each appears once."""
        out: List[Tuple[T, T]] = []
        if self.directed:
            for u, ns in self._adj.items():
                for v in ns:
                    out.append((u, v))
        else:
            seen: Set[Tuple[T, T]] = set()
            for u, ns in self._adj.items():
                for v in ns:
                    a, b = (u, v) if u <= v else (v, u)  # type: ignore[operator]
                    if (a, b) not in seen:
                        seen.add((a, b))
                        out.append((a, b))
        return out

    def __contains__(self, u: T) -> bool:
        return u in self._adj

    def __len__(self) -> int:
        return len(self._adj)

    def __repr__(self) -> str:
        kind = "DiGraph" if self.directed else "Graph"
        return f"{kind}(n={len(self._adj)})"

    @classmethod
    def from_edges(cls, edges: Iterable[Tuple[T, T]], *, directed: bool = False) -> "Graph[T]":
        g = cls(directed=directed)
        for u, v in edges:
            g.add_edge(u, v)
        return g


if __name__ == "__main__":
    g = Graph.from_edges([(1, 2), (2, 3), (3, 1)], directed=False)
    print(g, "nodes:", g.nodes(), "edges:", g.edges())
    print("neighbors(2):", g.neighbors(2))
