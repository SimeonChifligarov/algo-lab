import os
import sys

sys.path.append(os.path.dirname(__file__))

import unittest

from geometry_primitives import Point
from geometry_distances import (
    bounding_box,
    closest_pair_bruteforce,
    distance_between_parallel_lines,
    distance_between_segments,
    distance_point_to_ray,
    is_polygon_clockwise,
    is_polygon_counterclockwise,
    polygon_area,
    polygon_area_signed,
    polygon_perimeter,
    polyline_length,
    projection_parameter,
    projection_point_on_line,
    segment_length,
)
from segment_intersection import line_from_points, point_on_line


class TestGeometryDistances(unittest.TestCase):
    def test_distance_point_to_ray_projection_on_ray(self):
        p = Point(2, 3)
        a = Point(0, 0)
        b = Point(4, 0)

        self.assertAlmostEqual(distance_point_to_ray(p, a, b), 3.0)

    def test_distance_point_to_ray_before_origin(self):
        p = Point(-2, 1)
        a = Point(0, 0)
        b = Point(4, 0)

        self.assertAlmostEqual(distance_point_to_ray(p, a, b), 5 ** 0.5)

    def test_distance_point_to_ray_invalid(self):
        with self.assertRaises(ValueError):
            distance_point_to_ray(Point(1, 1), Point(0, 0), Point(0, 0))

    def test_projection_point_on_line(self):
        p = Point(2, 3)
        a = Point(0, 0)
        b = Point(4, 0)

        self.assertEqual(projection_point_on_line(p, a, b), Point(2, 0))

    def test_projection_parameter(self):
        a = Point(0, 0)
        b = Point(4, 0)

        self.assertAlmostEqual(projection_parameter(Point(2, 3), a, b), 0.5)
        self.assertAlmostEqual(projection_parameter(Point(-2, 1), a, b), -0.5)
        self.assertAlmostEqual(projection_parameter(Point(6, 1), a, b), 1.5)

    def test_projection_invalid(self):
        with self.assertRaises(ValueError):
            projection_point_on_line(Point(1, 1), Point(0, 0), Point(0, 0))
        with self.assertRaises(ValueError):
            projection_parameter(Point(1, 1), Point(0, 0), Point(0, 0))

    def test_distance_between_parallel_lines(self):
        a = Point(0, 0)
        b = Point(4, 0)
        c = Point(0, 3)
        d = Point(5, 3)

        self.assertAlmostEqual(distance_between_parallel_lines(a, b, c, d), 3.0)

    def test_distance_between_parallel_lines_invalid(self):
        with self.assertRaises(ValueError):
            distance_between_parallel_lines(Point(0, 0), Point(0, 0), Point(0, 1), Point(1, 1))

        with self.assertRaises(ValueError):
            distance_between_parallel_lines(Point(0, 0), Point(1, 0), Point(0, 0), Point(0, 1))

    def test_polygon_perimeter_closed(self):
        rect = [Point(0, 0), Point(4, 0), Point(4, 3), Point(0, 3)]
        self.assertAlmostEqual(polygon_perimeter(rect), 14.0)

    def test_polygon_perimeter_open(self):
        pts = [Point(0, 0), Point(3, 4), Point(6, 4)]
        self.assertAlmostEqual(polygon_perimeter(pts, closed=False), 8.0)

    def test_polygon_area(self):
        rect = [Point(0, 0), Point(4, 0), Point(4, 3), Point(0, 3)]
        self.assertAlmostEqual(polygon_area_signed(rect), 12.0)
        self.assertAlmostEqual(polygon_area(rect), 12.0)

    def test_polygon_orientation(self):
        ccw = [Point(0, 0), Point(4, 0), Point(4, 3), Point(0, 3)]
        cw = list(reversed(ccw))

        self.assertTrue(is_polygon_counterclockwise(ccw))
        self.assertFalse(is_polygon_clockwise(ccw))
        self.assertTrue(is_polygon_clockwise(cw))
        self.assertFalse(is_polygon_counterclockwise(cw))

    def test_bounding_box(self):
        pts = [Point(1, 2), Point(-1, 5), Point(4, 0)]
        self.assertEqual(bounding_box(pts), (Point(-1, 0), Point(4, 5)))

    def test_bounding_box_invalid(self):
        with self.assertRaises(ValueError):
            bounding_box([])

    def test_closest_pair_bruteforce(self):
        pts = [
            Point(0, 0),
            Point(2, 2),
            Point(2.5, 2.2),
            Point(10, 10),
            Point(3, 3),
        ]
        p1, p2, dist = closest_pair_bruteforce(pts)
        self.assertEqual({p1, p2}, {Point(2, 2), Point(2.5, 2.2)})
        self.assertAlmostEqual(dist, Point(2, 2).distance_to(Point(2.5, 2.2)))

    def test_closest_pair_bruteforce_none(self):
        self.assertIsNone(closest_pair_bruteforce([]))
        self.assertIsNone(closest_pair_bruteforce([Point(0, 0)]))

    def test_segment_length_and_polyline_length(self):
        self.assertAlmostEqual(segment_length(Point(0, 0), Point(3, 4)), 5.0)
        self.assertAlmostEqual(
            polyline_length([Point(0, 0), Point(1, 1), Point(4, 1)]),
            (2 ** 0.5) + 3.0,
        )

    def test_distance_between_segments_intersecting(self):
        a = Point(0, 0)
        b = Point(4, 4)
        c = Point(0, 4)
        d = Point(4, 0)

        self.assertEqual(distance_between_segments(a, b, c, d), 0.0)

    def test_distance_between_segments_disjoint(self):
        a = Point(0, 0)
        b = Point(2, 0)
        c = Point(3, 1)
        d = Point(3, 4)

        self.assertAlmostEqual(distance_between_segments(a, b, c, d), 2 ** 0.5)

    def test_interop_with_segment_module_helpers(self):
        line = line_from_points(Point(0, 0), Point(2, 2))
        self.assertTrue(point_on_line(Point(3, 3), Point(0, 0), Point(2, 2)))
        self.assertAlmostEqual(line.evaluate(Point(3, 3)), 0.0)


if __name__ == "__main__":
    unittest.main()
