import os
import sys

sys.path.append(os.path.dirname(__file__))

import unittest

from kruskal_mst import kruskal_mst


class TestKruskalMST(unittest.TestCase):
    def test_mst_on_known_graph(self):
        edges = [
            (4, 0, 1),
            (4, 0, 2),
            (2, 1, 2),
            (5, 1, 3),
            (10, 2, 3),
            (3, 2, 4),
            (7, 3, 4),
            (1, 3, 5),
            (8, 4, 5),
        ]

        mst_edges, total_weight = kruskal_mst(6, edges)

        self.assertEqual(len(mst_edges), 5)
        self.assertEqual(total_weight, 15)
        self.assertEqual(
            set(mst_edges),
            {
                (1, 3, 5),
                (2, 1, 2),
                (3, 2, 4),
                (4, 0, 1),
                (5, 1, 3),
            },
        )

    def test_edges_are_taken_in_greedy_order_without_cycles(self):
        edges = [
            (10, 0, 3),
            (1, 0, 1),
            (3, 1, 2),
            (2, 0, 2),
        ]

        mst_edges, total_weight = kruskal_mst(4, edges)

        self.assertEqual(len(mst_edges), 3)
        self.assertEqual(total_weight, 13)
        self.assertEqual(
            set(mst_edges),
            {
                (1, 0, 1),
                (2, 0, 2),
                (10, 0, 3),
            },
        )

    def test_single_vertex_graph(self):
        mst_edges, total_weight = kruskal_mst(1, [])

        self.assertEqual(mst_edges, [])
        self.assertEqual(total_weight, 0)

    def test_two_vertices_one_edge(self):
        mst_edges, total_weight = kruskal_mst(2, [(7, 0, 1)])

        self.assertEqual(mst_edges, [(7, 0, 1)])
        self.assertEqual(total_weight, 7)

    def test_negative_weights_are_supported(self):
        edges = [
            (-2, 0, 1),
            (3, 1, 2),
            (1, 0, 2),
        ]

        mst_edges, total_weight = kruskal_mst(3, edges)

        self.assertEqual(len(mst_edges), 2)
        self.assertEqual(total_weight, -1)
        self.assertEqual(
            set(mst_edges),
            {
                (-2, 0, 1),
                (1, 0, 2),
            },
        )

    def test_parallel_edges_choose_smaller_one(self):
        edges = [
            (10, 0, 1),
            (3, 0, 1),
            (2, 1, 2),
            (8, 0, 2),
        ]

        mst_edges, total_weight = kruskal_mst(3, edges)

        self.assertEqual(len(mst_edges), 2)
        self.assertEqual(total_weight, 5)
        self.assertEqual(
            set(mst_edges),
            {
                (3, 0, 1),
                (2, 1, 2),
            },
        )

    def test_disconnected_graph_raises_value_error(self):
        edges = [
            (1, 0, 1),
            (2, 2, 3),
        ]

        with self.assertRaises(ValueError):
            kruskal_mst(4, edges)

    def test_invalid_num_vertices_raises_value_error(self):
        with self.assertRaises(ValueError):
            kruskal_mst(0, [])

        with self.assertRaises(ValueError):
            kruskal_mst(-5, [])

    def test_invalid_vertex_negative_raises_index_error(self):
        edges = [
            (1, -1, 2),
        ]

        with self.assertRaises(IndexError):
            kruskal_mst(3, edges)

    def test_invalid_vertex_too_large_raises_index_error(self):
        edges = [
            (1, 0, 3),
        ]

        with self.assertRaises(IndexError):
            kruskal_mst(3, edges)

    def test_triangle_graph_skips_heaviest_cycle_edge(self):
        edges = [
            (1, 0, 1),
            (2, 1, 2),
            (3, 0, 2),
        ]

        mst_edges, total_weight = kruskal_mst(3, edges)

        self.assertEqual(len(mst_edges), 2)
        self.assertEqual(total_weight, 3)
        self.assertEqual(
            set(mst_edges),
            {
                (1, 0, 1),
                (2, 1, 2),
            },
        )


if __name__ == "__main__":
    unittest.main()
