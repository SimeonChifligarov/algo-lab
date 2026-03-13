"""
Topological Sort & DAGs — core directed graph utilities (Part 1/4)

This file defines a small adjacency-list Digraph tailored for DAG tasks:
- add_node, add_edge
- neighbors
- nodes, edges
- indegrees (needed for Kahn's algorithm)

Next files:
2) topo_sort.py            (Kahn + DFS postorder topo sort, cycle reporting)
3) dag_dp.py               (longest path in DAG via DP on topo order)
4) test_topo_and_dag.py    (unittest suite)

Nodes can be any hashable type.
Edges are stored as sets to avoid duplicates.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Generic, Hashable, Iterable, List, Set, Tuple, TypeVar

T = TypeVar("T", bound=Hashable)


@dataclass
class DiGraph(Generic[T]):
    _adj: Dict[T, Set[T]] = field(default_factory=dict)

    def add_node(self, u: T) -> None:
        if u not in self._adj:
            self._adj[u] = set()

    def add_edge(self, u: T, v: T) -> None:
        """Add directed edge u -> v (auto-add nodes)."""
        self.add_node(u)
        self.add_node(v)
        self._adj[u].add(v)

    def neighbors(self, u: T) -> Set[T]:
        return self._adj.get(u, set())

    def nodes(self) -> List[T]:
        return list(self._adj.keys())

    def edges(self) -> List[Tuple[T, T]]:
        out: List[Tuple[T, T]] = []
        for u, ns in self._adj.items():
            for v in ns:
                out.append((u, v))
        return out

    def indegrees(self) -> Dict[T, int]:
        """
        Compute indegree for each node.
        Ensures every node appears in the returned dict.
        """
        indeg: Dict[T, int] = {u: 0 for u in self._adj}
        for u, ns in self._adj.items():
            for v in ns:
                indeg[v] = indeg.get(v, 0) + 1
        return indeg

    def __contains__(self, u: T) -> bool:
        return u in self._adj

    def __len__(self) -> int:
        return len(self._adj)

    def __repr__(self) -> str:
        return f"DiGraph(n={len(self._adj)}, m={sum(len(v) for v in self._adj.values())})"

    @classmethod
    def from_edges(cls, edges: Iterable[Tuple[T, T]]) -> "DiGraph[T]":
        g = cls()
        for u, v in edges:
            g.add_edge(u, v)
        return g


if __name__ == "__main__":
    g = DiGraph.from_edges([("A", "C"), ("B", "C"), ("C", "D")])
    print(g)
    print("nodes:", g.nodes())
    print("edges:", g.edges())
    print("indeg:", g.indegrees())
