import os
import sys

sys.path.append(os.path.dirname(__file__))

import io
import unittest
from contextlib import redirect_stdout

from compare_and_demo import (
    compare_mst_results,
    main,
    print_graph,
    print_mst,
    union_find_cycle_demo,
)


class TestCompareAndDemo(unittest.TestCase):
    def test_print_graph_outputs_expected_lines(self):
        edges = [
            (4, 0, 1),
            (2, 1, 2),
        ]

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            print_graph(edges)

        output = buffer.getvalue()

        self.assertIn("Graph edges:", output)
        self.assertIn("0 -- 1  (weight=4)", output)
        self.assertIn("1 -- 2  (weight=2)", output)

    def test_print_mst_outputs_expected_lines(self):
        mst_edges = [
            (1, 3, 5),
            (2, 1, 2),
        ]
        total_weight = 3

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            print_mst("=== Example MST ===", mst_edges, total_weight)

        output = buffer.getvalue()

        self.assertIn("=== Example MST ===", output)
        self.assertIn("3 -- 5  (weight=1)", output)
        self.assertIn("1 -- 2  (weight=2)", output)
        self.assertIn("Total weight: 3", output)

    def test_compare_mst_results_same_weight_and_edge_count(self):
        kruskal_result = (
            [(1, 0, 1), (2, 1, 2)],
            3,
        )
        prim_result = (
            [(2, 1, 2), (1, 0, 1)],
            3,
        )

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            compare_mst_results(kruskal_result, prim_result)

        output = buffer.getvalue()

        self.assertIn("=== Comparison ===", output)
        self.assertIn("Kruskal edge count: 2", output)
        self.assertIn("Prim edge count:    2", output)
        self.assertIn("Kruskal weight:     3", output)
        self.assertIn("Prim weight:        3", output)
        self.assertIn("Both algorithms produced valid MST results", output)

    def test_compare_mst_results_different_weight(self):
        kruskal_result = (
            [(1, 0, 1), (2, 1, 2)],
            3,
        )
        prim_result = (
            [(1, 0, 1), (5, 1, 2)],
            6,
        )

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            compare_mst_results(kruskal_result, prim_result)

        output = buffer.getvalue()

        self.assertIn("The outputs differ", output)

    def test_union_find_cycle_demo_reports_cycle(self):
        edges = [
            (1, 0, 1),
            (2, 1, 2),
            (3, 0, 2),  # creates a cycle
            (4, 3, 4),
        ]

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            union_find_cycle_demo(5, edges)

        output = buffer.getvalue()

        self.assertIn("=== Union-Find Cycle Detection Demo ===", output)
        self.assertIn("Added edge 0 -- 1 (weight=1); no cycle created.", output)
        self.assertIn("Added edge 1 -- 2 (weight=2); no cycle created.", output)
        self.assertIn("Adding edge 0 -- 2 (weight=3) would create a cycle.", output)
        self.assertIn("Added edge 3 -- 4 (weight=4); no cycle created.", output)
        self.assertIn("Final groups:", output)

    def test_main_runs_and_prints_all_sections(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            main()

        output = buffer.getvalue()

        self.assertIn("=== Minimum Spanning Tree Demo ===", output)
        self.assertIn("Graph edges:", output)
        self.assertIn("=== Kruskal MST ===", output)
        self.assertIn("=== Prim MST ===", output)
        self.assertIn("=== Comparison ===", output)
        self.assertIn("=== Union-Find Cycle Detection Demo ===", output)

    def test_main_shows_matching_total_weight_for_both_algorithms(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            main()

        output = buffer.getvalue()

        self.assertIn("Kruskal weight:     15", output)
        self.assertIn("Prim weight:        15", output)


if __name__ == "__main__":
    unittest.main()
