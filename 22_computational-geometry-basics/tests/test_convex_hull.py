import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import unittest

from ..geometry_primitives import Point
from ..convex_hull import (
    convex_hull,
    convex_hull_vertices_only,
    convex_hull_with_boundary_points,
    extreme_points,
    hull_area,
    hull_edges,
    hull_perimeter,
    is_convex_polygon,
    point_in_convex_polygon,
)


class TestConvexHull(unittest.TestCase):
    def test_convex_hull_empty(self):
        self.assertEqual(convex_hull([]), [])

    def test_convex_hull_single_point(self):
        p = Point(1, 2)
        self.assertEqual(convex_hull([p]), [p])

    def test_convex_hull_two_points(self):
        pts = [Point(0, 0), Point(1, 1)]
        self.assertEqual(convex_hull(pts), [Point(0, 0), Point(1, 1)])

    def test_convex_hull_vertices_only(self):
        pts = [
            Point(0, 0),
            Point(1, 1),
            Point(2, 2),
            Point(0, 2),
            Point(2, 0),
            Point(1, 0.5),
            Point(1.5, 1.5),
            Point(0.5, 1.5),
            Point(2, 2),
            Point(0, 0),
        ]

        hull = convex_hull_vertices_only(pts)
        expected = [Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)]
        self.assertEqual(hull, expected)

    def test_convex_hull_with_boundary_points_all_collinear(self):
        pts = [Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0), Point(2, 0)]
        hull = convex_hull_with_boundary_points(pts)
        self.assertEqual(hull, [Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0)])

    def test_convex_hull_vertices_only_all_collinear(self):
        pts = [Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0)]
        hull = convex_hull_vertices_only(pts)
        self.assertEqual(hull, [Point(0, 0), Point(3, 0)])

    def test_convex_hull_removes_duplicates(self):
        pts = [Point(0, 0), Point(1, 0), Point(0, 1), Point(0, 0), Point(1, 0)]
        hull = convex_hull_vertices_only(pts)
        self.assertEqual(hull, [Point(0, 0), Point(1, 0), Point(0, 1)])

    def test_is_convex_polygon(self):
        square = [Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)]
        non_convex = [Point(0, 0), Point(2, 0), Point(1, 1), Point(2, 2), Point(0, 2)]

        self.assertTrue(is_convex_polygon(square))
        self.assertFalse(is_convex_polygon(non_convex))

    def test_is_convex_polygon_strict(self):
        polygon_with_collinear = [Point(0, 0), Point(1, 0), Point(2, 0), Point(2, 1), Point(0, 1)]
        self.assertTrue(is_convex_polygon(polygon_with_collinear, strict=False))
        self.assertFalse(is_convex_polygon(polygon_with_collinear, strict=True))

    def test_point_in_convex_polygon_inside(self):
        square = [Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)]
        self.assertTrue(point_in_convex_polygon(Point(1, 1), square))

    def test_point_in_convex_polygon_boundary(self):
        square = [Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)]
        self.assertTrue(point_in_convex_polygon(Point(2, 1), square))
        self.assertTrue(point_in_convex_polygon(Point(0, 0), square))

    def test_point_in_convex_polygon_outside(self):
        square = [Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)]
        self.assertFalse(point_in_convex_polygon(Point(3, 1), square))

    def test_point_in_convex_polygon_small_cases(self):
        self.assertFalse(point_in_convex_polygon(Point(0, 0), []))
        self.assertTrue(point_in_convex_polygon(Point(1, 1), [Point(1, 1)]))
        self.assertFalse(point_in_convex_polygon(Point(2, 2), [Point(1, 1)]))
        self.assertTrue(point_in_convex_polygon(Point(1, 0), [Point(0, 0), Point(2, 0)]))

    def test_hull_area(self):
        pts = [
            Point(0, 0),
            Point(2, 0),
            Point(2, 2),
            Point(0, 2),
            Point(1, 1),
        ]
        self.assertAlmostEqual(hull_area(pts), 4.0)

    def test_hull_perimeter_polygon(self):
        pts = [
            Point(0, 0),
            Point(2, 0),
            Point(2, 2),
            Point(0, 2),
            Point(1, 1),
        ]
        self.assertAlmostEqual(hull_perimeter(pts), 8.0)

    def test_hull_perimeter_two_points(self):
        pts = [Point(0, 0), Point(3, 4)]
        self.assertAlmostEqual(hull_perimeter(pts), 10.0)

    def test_extreme_points(self):
        pts = [Point(0, 0), Point(1, 1), Point(2, 0), Point(1, 0.5)]
        self.assertEqual(extreme_points(pts), convex_hull_vertices_only(pts))

    def test_hull_edges(self):
        hull = [Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)]
        self.assertEqual(
            hull_edges(hull),
            [
                (Point(0, 0), Point(2, 0)),
                (Point(2, 0), Point(2, 2)),
                (Point(2, 2), Point(0, 2)),
                (Point(0, 2), Point(0, 0)),
            ],
        )

    def test_hull_edges_small_cases(self):
        self.assertEqual(hull_edges([]), [])
        self.assertEqual(hull_edges([Point(0, 0)]), [])
        self.assertEqual(hull_edges([Point(0, 0), Point(1, 1)]), [(Point(0, 0), Point(1, 1))])


if __name__ == "__main__":
    unittest.main()
