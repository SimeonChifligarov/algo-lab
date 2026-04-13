"""
Tests for Shortest Paths toolkit (Part 4/4)

Run:
  python test_shortest_paths.py

or:
  python -m unittest test_shortest_paths.py

Covers:
- Dijkstra correctness on non-negative weights + path reconstruction
- Dijkstra rejects negative edges
- Bellman–Ford correctness with negative edges
- Bellman–Ford detects negative cycles
"""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

# Make local imports work even if tests are launched from repo root
THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from ..weighted_graph import WeightedDiGraph
from ..dijkstra import dijkstra_distances, dijkstra_shortest_path
from ..bellman_ford import bellman_ford, bellman_ford_shortest_path


class TestDijkstra(unittest.TestCase):
    def test_dijkstra_basic(self) -> None:
        g = WeightedDiGraph.from_edges([
            ("A", "B", 1),
            ("B", "C", 2),
            ("A", "C", 10),
            ("C", "D", 1),
            ("B", "D", 10),
        ])
        dist = dijkstra_distances(g, "A")
        self.assertEqual(dist["A"], 0.0)
        self.assertEqual(dist["B"], 1.0)
        self.assertEqual(dist["C"], 3.0)
        self.assertEqual(dist["D"], 4.0)

        path = dijkstra_shortest_path(g, "A", "D")
        self.assertEqual(path, ["A", "B", "C", "D"])

    def test_dijkstra_unreachable(self) -> None:
        g = WeightedDiGraph.from_edges([
            (1, 2, 1),
            (3, 4, 1),
        ])
        self.assertIsNone(dijkstra_shortest_path(g, 1, 4))

    def test_dijkstra_negative_rejected(self) -> None:
        g = WeightedDiGraph.from_edges([
            ("A", "B", -1),
        ])
        with self.assertRaises(ValueError):
            dijkstra_distances(g, "A")

    def test_dijkstra_start_missing(self) -> None:
        g = WeightedDiGraph.from_edges([(1, 2, 1)])
        with self.assertRaises(KeyError):
            dijkstra_distances(g, 999)


class TestBellmanFord(unittest.TestCase):
    def test_bellman_ford_negative_edges_no_cycle(self) -> None:
        g = WeightedDiGraph.from_edges([
            ("A", "B", 1),
            ("A", "C", 4),
            ("B", "C", -2),
            ("B", "D", 2),
            ("C", "D", 3),
        ])
        dist, parent, cycle = bellman_ford(g, "A")
        self.assertIsNone(cycle)
        self.assertAlmostEqual(dist["D"], 2.0)  # A->B->C->D = 1 + (-2) + 3 = 2

        path = bellman_ford_shortest_path(g, "A", "D")
        self.assertEqual(path, ["A", "B", "C", "D"])

    def test_bellman_ford_negative_cycle_detected(self) -> None:
        g = WeightedDiGraph.from_edges([
            ("A", "B", 1),
            ("B", "C", 1),
            ("C", "B", -3),  # cycle B<->C has weight -2
        ])
        dist, parent, cycle = bellman_ford(g, "A")
        self.assertIsNotNone(cycle)
        self.assertTrue(len(cycle) >= 2)

        with self.assertRaises(ValueError):
            bellman_ford_shortest_path(g, "A", "C")

    def test_bellman_ford_unreachable(self) -> None:
        g = WeightedDiGraph.from_edges([
            (1, 2, 1),
            (3, 4, 1),
        ])
        path = bellman_ford_shortest_path(g, 1, 4)
        self.assertIsNone(path)

    def test_bellman_ford_start_missing(self) -> None:
        g = WeightedDiGraph.from_edges([(1, 2, 1)])
        with self.assertRaises(KeyError):
            bellman_ford(g, 999)


if __name__ == "__main__":
    unittest.main(verbosity=2)
