"""
Tests for Topological Sort & DAGs toolkit (Part 4/4)

Run:
  python test_topo_and_dag.py

or:
  python -m unittest test_topo_and_dag.py

Covers:
- Kahn topological sort (including lexicographic)
- DFS postorder topological sort
- cycle detection and cycle reporting
- longest path in DAG (unweighted and weighted)
"""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

# Make local imports work even if tests are launched from repo root
THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from ..dag_core import DiGraph
from ..topo_sort import topo_kahn, topo_dfs, is_dag, find_cycle
from ..dag_dp import longest_path_dag, longest_path_dag_weighted


def _is_valid_topo(order, edges) -> bool:
    pos = {node: i for i, node in enumerate(order)}
    for u, v in edges:
        if pos[u] >= pos[v]:
            return False
    return True


class TestTopoSort(unittest.TestCase):
    def test_kahn_topo(self) -> None:
        g = DiGraph.from_edges([("A", "C"), ("B", "C"), ("C", "D")])
        order = topo_kahn(g)
        self.assertEqual(set(order), {"A", "B", "C", "D"})
        self.assertTrue(_is_valid_topo(order, g.edges()))

    def test_kahn_lexicographic(self) -> None:
        g = DiGraph.from_edges([("A", "C"), ("B", "C"), ("C", "D")])
        order = topo_kahn(g, lexicographic=True)
        # With lexicographic, A then B should appear before C
        self.assertEqual(order[:2], ["A", "B"])
        self.assertTrue(_is_valid_topo(order, g.edges()))

    def test_dfs_topo(self) -> None:
        g = DiGraph.from_edges([("A", "C"), ("B", "C"), ("C", "D")])
        order = topo_dfs(g)
        self.assertEqual(set(order), {"A", "B", "C", "D"})
        self.assertTrue(_is_valid_topo(order, g.edges()))

    def test_cycle_detection(self) -> None:
        cyc = DiGraph.from_edges([(1, 2), (2, 3), (3, 1)])
        self.assertFalse(is_dag(cyc))
        cyc_list = find_cycle(cyc)
        self.assertTrue(cyc_list)  # non-empty
        with self.assertRaises(ValueError):
            topo_kahn(cyc)
        with self.assertRaises(ValueError):
            topo_dfs(cyc)

        # basic cycle shape: first==last or contains repetition
        self.assertTrue(cyc_list[0] == cyc_list[-1] or len(set(cyc_list)) < len(cyc_list))


class TestDagDP(unittest.TestCase):
    def test_longest_path_unweighted(self) -> None:
        # A -> B -> C -> D (and A->C shortcut)
        g = DiGraph.from_edges([("A", "B"), ("B", "C"), ("A", "C"), ("C", "D")])
        length, path = longest_path_dag(g)
        self.assertEqual(length, 3)
        self.assertEqual(path[0], "A")
        self.assertEqual(path[-1], "D")
        self.assertTrue(_is_valid_topo(path, list(zip(path, path[1:]))))

    def test_longest_path_weighted(self) -> None:
        g = DiGraph.from_edges([("A", "B"), ("B", "C"), ("A", "C"), ("C", "D")])
        weights = {("A", "B"): 2.0, ("B", "C"): 3.0, ("A", "C"): 10.0, ("C", "D"): 1.0}
        best, path = longest_path_dag_weighted(g, weights)
        # Best is A->C->D with weight 11
        self.assertEqual(best, 11.0)
        self.assertEqual(path, ["A", "C", "D"])

    def test_empty_graph(self) -> None:
        g = DiGraph()
        self.assertEqual(longest_path_dag(g), (0, []))
        self.assertEqual(longest_path_dag_weighted(g, {}), (0.0, []))


if __name__ == "__main__":
    unittest.main(verbosity=2)
