"""
Tests for Graphs Basics (BFS/DFS) toolkit (Part 4/4)

Run:
  python test_graphs.py

or:
  python -m unittest test_graphs.py
"""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

# Make local imports work even if tests are launched from repo root
THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from graph_core import Graph
from bfs_shortest_path import bfs_parents, bfs_distances, bfs_shortest_path
from dfs_algorithms import (
    dfs_reachable,
    connected_components,
    has_cycle_undirected,
    has_cycle_directed,
)


class TestGraphCore(unittest.TestCase):
    def test_add_and_neighbors(self) -> None:
        g = Graph[int](directed=False)
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        self.assertIn(1, g)
        self.assertEqual(g.neighbors(2), {1, 3})
        self.assertEqual(g.neighbors(999), set())

    def test_directed_edges(self) -> None:
        g = Graph.from_edges([(1, 2), (2, 3)], directed=True)
        self.assertEqual(g.neighbors(1), {2})
        self.assertEqual(g.neighbors(2), {3})
        self.assertEqual(g.neighbors(3), set())

    def test_edges_undirected(self) -> None:
        g = Graph.from_edges([(1, 2), (2, 1), (2, 3)], directed=False)
        # stored as sets, so duplicates collapse
        e = set(g.edges())
        self.assertEqual(e, {(1, 2), (2, 3)})


class TestBFS(unittest.TestCase):
    def test_bfs_parents_and_path(self) -> None:
        g = Graph.from_edges(
            [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")],
            directed=False,
        )
        parent = bfs_parents(g, "A")
        self.assertIsNone(parent["A"])
        self.assertIn("E", parent)

        path = bfs_shortest_path(g, "A", "E")
        self.assertEqual(path[0], "A")
        self.assertEqual(path[-1], "E")
        # path length should be 4 nodes: A -> (B or C) -> D -> E
        self.assertEqual(len(path), 4)

    def test_bfs_distances(self) -> None:
        g = Graph.from_edges([(1, 2), (2, 3), (1, 4)], directed=False)
        dist = bfs_distances(g, 1)
        self.assertEqual(dist[1], 0)
        self.assertEqual(dist[2], 1)
        self.assertEqual(dist[4], 1)
        self.assertEqual(dist[3], 2)

    def test_bfs_unreachable(self) -> None:
        g = Graph.from_edges([(1, 2), (3, 4)], directed=False)
        self.assertIsNone(bfs_shortest_path(g, 1, 4))

    def test_bfs_start_missing(self) -> None:
        g = Graph.from_edges([(1, 2)], directed=False)
        with self.assertRaises(KeyError):
            bfs_parents(g, 999)


class TestDFS(unittest.TestCase):
    def test_dfs_reachable(self) -> None:
        g = Graph.from_edges([(1, 2), (2, 3), (3, 4)], directed=False)
        self.assertEqual(dfs_reachable(g, 2), {1, 2, 3, 4})

    def test_connected_components(self) -> None:
        g = Graph.from_edges([(1, 2), (3, 4), (4, 5)], directed=False)
        comps = connected_components(g)
        # compare as sets of frozensets ignoring order
        got = {frozenset(c) for c in comps}
        self.assertEqual(got, {frozenset({1, 2}), frozenset({3, 4, 5})})

        dg = Graph.from_edges([(1, 2)], directed=True)
        with self.assertRaises(ValueError):
            connected_components(dg)

    def test_cycle_undirected(self) -> None:
        g1 = Graph.from_edges([(1, 2), (2, 3), (3, 1)], directed=False)
        self.assertTrue(has_cycle_undirected(g1))

        g2 = Graph.from_edges([(1, 2), (2, 3)], directed=False)
        self.assertFalse(has_cycle_undirected(g2))

        dg = Graph.from_edges([(1, 2)], directed=True)
        with self.assertRaises(ValueError):
            has_cycle_undirected(dg)

    def test_cycle_directed(self) -> None:
        g1 = Graph.from_edges([(1, 2), (2, 3), (3, 1)], directed=True)
        self.assertTrue(has_cycle_directed(g1))

        g2 = Graph.from_edges([(1, 2), (2, 3), (3, 4)], directed=True)
        self.assertFalse(has_cycle_directed(g2))

        ug = Graph.from_edges([(1, 2)], directed=False)
        with self.assertRaises(ValueError):
            has_cycle_directed(ug)


if __name__ == "__main__":
    unittest.main(verbosity=2)
