import os
import sys

sys.path.append(os.path.dirname(__file__))

import unittest

from prim_mst import build_adjacency_list, prim_mst


class TestBuildAdjacencyList(unittest.TestCase):
    def test_builds_undirected_adjacency_list(self):
        edges = [
            (4, 0, 1),
            (2, 1, 2),
            (7, 0, 2),
        ]

        adj = build_adjacency_list(3, edges)

        self.assertEqual(adj[0], [(1, 4), (2, 7)])
        self.assertEqual(adj[1], [(0, 4), (2, 2)])
        self.assertEqual(adj[2], [(1, 2), (0, 7)])

    def test_invalid_num_vertices_raises_value_error(self):
        with self.assertRaises(ValueError):
            build_adjacency_list(0, [])

        with self.assertRaises(ValueError):
            build_adjacency_list(-1, [])

    def test_invalid_vertex_negative_raises_index_error(self):
        with self.assertRaises(IndexError):
            build_adjacency_list(3, [(1, -1, 2)])

    def test_invalid_vertex_too_large_raises_index_error(self):
        with self.assertRaises(IndexError):
            build_adjacency_list(3, [(1, 0, 3)])


class TestPrimMST(unittest.TestCase):
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

        mst_edges, total_weight = prim_mst(6, edges, start=0)

        self.assertEqual(len(mst_edges), 5)
        self.assertEqual(total_weight, 15)
        self.assertEqual(
            set(mst_edges),
            {
                (4, 0, 1),
                (2, 1, 2),
                (3, 2, 4),
                (5, 1, 3),
                (1, 3, 5),
            },
        )

    def test_same_total_weight_from_different_start_vertex(self):
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

        mst_edges, total_weight = prim_mst(6, edges, start=3)

        self.assertEqual(len(mst_edges), 5)
        self.assertEqual(total_weight, 15)

    def test_single_vertex_graph(self):
        mst_edges, total_weight = prim_mst(1, [], start=0)

        self.assertEqual(mst_edges, [])
        self.assertEqual(total_weight, 0)

    def test_two_vertices_one_edge(self):
        mst_edges, total_weight = prim_mst(2, [(7, 0, 1)], start=0)

        self.assertEqual(mst_edges, [(7, 0, 1)])
        self.assertEqual(total_weight, 7)

    def test_negative_weights_are_supported(self):
        edges = [
            (-2, 0, 1),
            (3, 1, 2),
            (1, 0, 2),
        ]

        mst_edges, total_weight = prim_mst(3, edges, start=0)

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

        mst_edges, total_weight = prim_mst(3, edges, start=0)

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
            prim_mst(4, edges, start=0)

    def test_invalid_num_vertices_raises_value_error(self):
        with self.assertRaises(ValueError):
            prim_mst(0, [], start=0)

        with self.assertRaises(ValueError):
            prim_mst(-2, [], start=0)

    def test_invalid_start_vertex_negative_raises_index_error(self):
        with self.assertRaises(IndexError):
            prim_mst(3, [(1, 0, 1)], start=-1)

    def test_invalid_start_vertex_too_large_raises_index_error(self):
        with self.assertRaises(IndexError):
            prim_mst(3, [(1, 0, 1)], start=3)

    def test_invalid_edge_vertex_raises_index_error(self):
        with self.assertRaises(IndexError):
            prim_mst(3, [(1, 0, 3)], start=0)

    def test_triangle_graph_skips_heaviest_cycle_edge(self):
        edges = [
            (1, 0, 1),
            (2, 1, 2),
            (3, 0, 2),
        ]

        mst_edges, total_weight = prim_mst(3, edges, start=0)

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
