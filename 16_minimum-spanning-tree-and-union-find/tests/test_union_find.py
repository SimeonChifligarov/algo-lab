import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import unittest

from ..union_find import UnionFind


class TestUnionFind(unittest.TestCase):
    def test_initial_state(self):
        uf = UnionFind(5)

        self.assertEqual(uf.parent, [0, 1, 2, 3, 4])
        self.assertEqual(uf.rank, [0, 0, 0, 0, 0])
        self.assertEqual(uf.count_components(), 5)
        self.assertEqual(
            uf.groups(),
            {
                0: [0],
                1: [1],
                2: [2],
                3: [3],
                4: [4],
            },
        )

    def test_invalid_size(self):
        with self.assertRaises(ValueError):
            UnionFind(0)

        with self.assertRaises(ValueError):
            UnionFind(-3)

    def test_find_returns_own_root_initially(self):
        uf = UnionFind(4)

        self.assertEqual(uf.find(0), 0)
        self.assertEqual(uf.find(1), 1)
        self.assertEqual(uf.find(2), 2)
        self.assertEqual(uf.find(3), 3)

    def test_union_merges_two_sets(self):
        uf = UnionFind(4)

        merged = uf.union(0, 1)

        self.assertTrue(merged)
        self.assertTrue(uf.connected(0, 1))
        self.assertEqual(uf.count_components(), 3)

    def test_union_returns_false_when_already_connected(self):
        uf = UnionFind(4)

        self.assertTrue(uf.union(0, 1))
        self.assertFalse(uf.union(0, 1))
        self.assertFalse(uf.union(1, 0))
        self.assertEqual(uf.count_components(), 3)

    def test_connected(self):
        uf = UnionFind(6)

        uf.union(0, 1)
        uf.union(1, 2)
        uf.union(4, 5)

        self.assertTrue(uf.connected(0, 2))
        self.assertFalse(uf.connected(0, 3))
        self.assertTrue(uf.connected(4, 5))
        self.assertFalse(uf.connected(2, 5))

    def test_groups_after_multiple_unions(self):
        uf = UnionFind(6)

        uf.union(0, 1)
        uf.union(1, 2)
        uf.union(3, 4)

        groups = uf.groups()
        normalized = {root: sorted(members) for root, members in groups.items()}
        member_sets = sorted(normalized.values())

        self.assertEqual(member_sets, [[0, 1, 2], [3, 4], [5]])

    def test_path_compression_effect(self):
        uf = UnionFind(5)

        uf.union(0, 1)
        uf.union(1, 2)
        uf.union(2, 3)

        root_before = uf.find(3)
        self.assertEqual(root_before, uf.find(0))

        # After calling find, path compression should make parent[3]
        # point directly to the root.
        self.assertEqual(uf.parent[3], uf.find(0))

    def test_union_by_rank_keeps_same_root_for_connected_nodes(self):
        uf = UnionFind(6)

        uf.union(0, 1)
        uf.union(2, 3)
        uf.union(0, 2)

        root = uf.find(0)
        self.assertEqual(uf.find(1), root)
        self.assertEqual(uf.find(2), root)
        self.assertEqual(uf.find(3), root)

    def test_invalid_find_raises_index_error(self):
        uf = UnionFind(3)

        with self.assertRaises(IndexError):
            uf.find(-1)

        with self.assertRaises(IndexError):
            uf.find(3)

    def test_invalid_union_raises_index_error(self):
        uf = UnionFind(3)

        with self.assertRaises(IndexError):
            uf.union(-1, 1)

        with self.assertRaises(IndexError):
            uf.union(0, 3)

    def test_invalid_connected_raises_index_error(self):
        uf = UnionFind(3)

        with self.assertRaises(IndexError):
            uf.connected(5, 1)

        with self.assertRaises(IndexError):
            uf.connected(0, -2)


if __name__ == "__main__":
    unittest.main()
