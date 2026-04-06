import os
import sys

sys.path.append(os.path.dirname(__file__))

import unittest

from geometry_primitives import Point
from segment_intersection import (
    Line,
    bounding_boxes_overlap,
    distance_point_to_line,
    distance_point_to_segment,
    line_from_points,
    line_intersection,
    point_on_line,
    point_on_segment,
    segment_intersection_point,
    segment_intersection_type,
    segments_intersect,
)


class TestSegmentIntersection(unittest.TestCase):
    def test_line_evaluate_and_normalized(self):
        line = Line(2, 0, -4)
        self.assertEqual(line.evaluate(Point(2, 10)), 0)

        normalized = line.normalized()
        self.assertAlmostEqual(normalized.a ** 2 + normalized.b ** 2, 1.0)

    def test_normalize_degenerate_line(self):
        with self.assertRaises(ValueError):
            Line(0, 0, 1).normalized()

    def test_line_from_points(self):
        line = line_from_points(Point(0, 0), Point(2, 2))
        self.assertAlmostEqual(line.evaluate(Point(1, 1)), 0.0)
        self.assertAlmostEqual(line.evaluate(Point(3, 3)), 0.0)

    def test_line_from_points_invalid(self):
        with self.assertRaises(ValueError):
            line_from_points(Point(1, 1), Point(1, 1))

    def test_point_on_line(self):
        a = Point(0, 0)
        b = Point(2, 2)
        self.assertTrue(point_on_line(Point(3, 3), a, b))
        self.assertFalse(point_on_line(Point(3, 4), a, b))

    def test_point_on_segment(self):
        a = Point(0, 0)
        b = Point(4, 4)
        self.assertTrue(point_on_segment(Point(2, 2), a, b))
        self.assertTrue(point_on_segment(Point(0, 0), a, b))
        self.assertTrue(point_on_segment(Point(4, 4), a, b))
        self.assertFalse(point_on_segment(Point(5, 5), a, b))
        self.assertFalse(point_on_segment(Point(2, 3), a, b))

    def test_bounding_boxes_overlap(self):
        self.assertTrue(
            bounding_boxes_overlap(Point(0, 0), Point(2, 2), Point(1, 1), Point(3, 3))
        )
        self.assertFalse(
            bounding_boxes_overlap(Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 3))
        )

    def test_segments_intersect_proper(self):
        a = Point(0, 0)
        b = Point(4, 4)
        c = Point(0, 4)
        d = Point(4, 0)

        self.assertTrue(segments_intersect(a, b, c, d))
        self.assertEqual(segment_intersection_type(a, b, c, d), "proper")
        self.assertEqual(segment_intersection_point(a, b, c, d), Point(2, 2))

    def test_segments_intersect_touching_endpoint(self):
        a = Point(0, 0)
        b = Point(4, 0)
        c = Point(4, 0)
        d = Point(6, 2)

        self.assertTrue(segments_intersect(a, b, c, d))
        self.assertEqual(segment_intersection_type(a, b, c, d), "touching")
        self.assertEqual(segment_intersection_point(a, b, c, d), Point(4, 0))

    def test_segments_overlap_collinear(self):
        a = Point(0, 0)
        b = Point(6, 0)
        c = Point(2, 0)
        d = Point(4, 0)

        self.assertTrue(segments_intersect(a, b, c, d))
        self.assertEqual(segment_intersection_type(a, b, c, d), "overlapping")
        self.assertIsNone(segment_intersection_point(a, b, c, d))

    def test_segments_disjoint(self):
        a = Point(0, 0)
        b = Point(2, 2)
        c = Point(3, 3)
        d = Point(5, 5)

        self.assertFalse(segments_intersect(a, b, c, d))
        self.assertEqual(segment_intersection_type(a, b, c, d), "none")
        self.assertIsNone(segment_intersection_point(a, b, c, d))

    def test_line_intersection(self):
        a = Point(0, 0)
        b = Point(4, 4)
        c = Point(0, 4)
        d = Point(4, 0)

        self.assertEqual(line_intersection(a, b, c, d), Point(2, 2))

    def test_line_intersection_parallel(self):
        a = Point(0, 0)
        b = Point(4, 0)
        c = Point(0, 2)
        d = Point(4, 2)

        self.assertIsNone(line_intersection(a, b, c, d))

    def test_distance_point_to_line(self):
        p = Point(2, 3)
        a = Point(0, 0)
        b = Point(4, 0)

        self.assertAlmostEqual(distance_point_to_line(p, a, b), 3.0)

    def test_distance_point_to_line_invalid(self):
        with self.assertRaises(ValueError):
            distance_point_to_line(Point(1, 1), Point(0, 0), Point(0, 0))

    def test_distance_point_to_segment_projection_inside(self):
        p = Point(2, 3)
        a = Point(0, 0)
        b = Point(4, 0)

        self.assertAlmostEqual(distance_point_to_segment(p, a, b), 3.0)

    def test_distance_point_to_segment_nearest_endpoint(self):
        p = Point(-1, 2)
        a = Point(0, 0)
        b = Point(4, 0)

        self.assertAlmostEqual(distance_point_to_segment(p, a, b), 5 ** 0.5)

    def test_distance_point_to_degenerate_segment(self):
        p = Point(1, 1)
        a = Point(0, 0)
        b = Point(0, 0)

        self.assertAlmostEqual(distance_point_to_segment(p, a, b), 2 ** 0.5)


if __name__ == "__main__":
    unittest.main()
