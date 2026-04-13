import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import unittest

from ..geometry_primitives import (
    EPSILON,
    Point,
    almost_equal,
    are_collinear,
    centroid,
    chebyshev_distance,
    cross,
    cross_three,
    distance_between_points,
    dot,
    manhattan_distance,
    midpoint,
    orientation,
    orientation_name,
    triangle_area,
    triangle_area_signed,
)


class TestGeometryPrimitives(unittest.TestCase):
    def test_almost_equal(self):
        self.assertTrue(almost_equal(1.0, 1.0 + 1e-10))
        self.assertFalse(almost_equal(1.0, 1.0 + 1e-4))

    def test_point_arithmetic(self):
        a = Point(1, 2)
        b = Point(3, 5)

        self.assertEqual(a + b, Point(4, 7))
        self.assertEqual(b - a, Point(2, 3))
        self.assertEqual(2 * a, Point(2, 4))
        self.assertEqual(a * 3, Point(3, 6))
        self.assertEqual(b / 2, Point(1.5, 2.5))

    def test_point_division_by_zero(self):
        with self.assertRaises(ValueError):
            _ = Point(1, 2) / 0

    def test_point_helpers(self):
        p = Point(3, 4)
        self.assertEqual(p.as_tuple(), (3, 4))
        self.assertAlmostEqual(p.norm(), 5.0)
        self.assertEqual(p.norm_squared(), 25)

    def test_distance_methods(self):
        a = Point(0, 0)
        b = Point(3, 4)

        self.assertAlmostEqual(a.distance_to(b), 5.0)
        self.assertEqual(a.distance_squared_to(b), 25)
        self.assertAlmostEqual(distance_between_points(a, b), 5.0)
        self.assertEqual(manhattan_distance(a, b), 7)
        self.assertEqual(chebyshev_distance(a, b), 4)

    def test_dot_and_cross(self):
        a = Point(1, 2)
        b = Point(3, 4)

        self.assertEqual(dot(a, b), 11)
        self.assertEqual(cross(a, b), -2)

    def test_cross_three(self):
        a = Point(0, 0)
        b = Point(2, 0)
        c = Point(1, 1)
        self.assertEqual(cross_three(a, b, c), 2)

    def test_orientation_counterclockwise(self):
        a = Point(0, 0)
        b = Point(2, 0)
        c = Point(1, 1)

        self.assertEqual(orientation(a, b, c), 1)
        self.assertEqual(orientation_name(a, b, c), "counterclockwise")

    def test_orientation_clockwise(self):
        a = Point(0, 0)
        b = Point(2, 0)
        c = Point(1, -1)

        self.assertEqual(orientation(a, b, c), -1)
        self.assertEqual(orientation_name(a, b, c), "clockwise")

    def test_orientation_collinear(self):
        a = Point(0, 0)
        b = Point(2, 0)
        c = Point(5, 0)

        self.assertEqual(orientation(a, b, c), 0)
        self.assertEqual(orientation_name(a, b, c), "collinear")
        self.assertTrue(are_collinear(a, b, c))

    def test_orientation_with_epsilon(self):
        a = Point(0, 0)
        b = Point(1, 0)
        c = Point(1, EPSILON / 10)

        self.assertEqual(orientation(a, b, c), 0)

    def test_midpoint(self):
        a = Point(0, 0)
        b = Point(4, 6)
        self.assertEqual(midpoint(a, b), Point(2, 3))

    def test_triangle_area(self):
        a = Point(0, 0)
        b = Point(4, 0)
        c = Point(0, 3)

        self.assertAlmostEqual(triangle_area_signed(a, b, c), 6.0)
        self.assertAlmostEqual(triangle_area(a, b, c), 6.0)
        self.assertAlmostEqual(triangle_area_signed(a, c, b), -6.0)

    def test_centroid(self):
        pts = [Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)]
        self.assertEqual(centroid(pts), Point(1, 1))

    def test_centroid_invalid(self):
        with self.assertRaises(ValueError):
            centroid([])


if __name__ == "__main__":
    unittest.main()
