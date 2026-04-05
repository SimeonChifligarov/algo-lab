"""
Distance formulas and basic geometry primitives.

This module builds on geometry_primitives.py and segment_intersection.py.

It focuses on:
- distance between points
- distance from point to line
- distance from point to ray
- distance from point to segment
- distance between parallel lines
- perimeter / polygon length helpers
- polygon area
- simple closest-pair brute force utility for learning

This file is meant to strengthen geometric intuition before moving on
to convex hull construction.
"""

from __future__ import annotations

from math import inf
from typing import Iterable, List, Optional, Sequence, Tuple

from geometry_primitives import (
    EPSILON,
    Point,
    almost_equal,
    cross,
    distance_between_points,
    dot,
)
from segment_intersection import (
    distance_point_to_line,
    distance_point_to_segment,
    line_from_points,
    point_on_line,
    segments_intersect,
)


def distance_point_to_ray(p: Point, a: Point, b: Point) -> float:
    """
    Distance from point p to the ray starting at a and going through b.

    Args:
        p: query point
        a: ray origin
        b: another point determining direction

    Returns:
        Minimum Euclidean distance from p to the ray.

    Raises:
        ValueError: if a and b are the same point
    """
    ab = b - a
    ap = p - a

    ab_len_sq = dot(ab, ab)
    if almost_equal(ab_len_sq, 0.0):
        raise ValueError("Ray requires two distinct points")

    t = dot(ap, ab) / ab_len_sq

    if t < 0.0:
        return p.distance_to(a)

    projection = a + ab * t
    return p.distance_to(projection)


def projection_point_on_line(p: Point, a: Point, b: Point) -> Point:
    """
    Orthogonal projection of point p onto the infinite line through a and b.

    Args:
        p: query point
        a, b: distinct points defining the line

    Returns:
        Projected point on the line.

    Raises:
        ValueError: if a and b are the same point
    """
    ab = b - a
    ab_len_sq = dot(ab, ab)

    if almost_equal(ab_len_sq, 0.0):
        raise ValueError("Line requires two distinct points")

    t = dot(p - a, ab) / ab_len_sq
    return a + ab * t


def projection_parameter(p: Point, a: Point, b: Point) -> float:
    """
    Return the parameter t such that projection of p on line AB is:

        a + t * (b - a)

    Interpretation:
        t < 0   -> before point a
        0..1    -> on segment [a, b]
        t > 1   -> beyond point b
    """
    ab = b - a
    ab_len_sq = dot(ab, ab)

    if almost_equal(ab_len_sq, 0.0):
        raise ValueError("Line requires two distinct points")

    return dot(p - a, ab) / ab_len_sq


def distance_between_parallel_lines(
        a: Point,
        b: Point,
        c: Point,
        d: Point,
        eps: float = EPSILON,
) -> float:
    """
    Distance between two parallel infinite lines AB and CD.

    Args:
        a, b: define first line
        c, d: define second line

    Returns:
        Distance between the two lines.

    Raises:
        ValueError: if either line is degenerate or if the lines are not parallel
    """
    ab = b - a
    cd = d - c

    if almost_equal(dot(ab, ab), 0.0):
        raise ValueError("First line is degenerate")
    if almost_equal(dot(cd, cd), 0.0):
        raise ValueError("Second line is degenerate")

    if abs(cross(ab, cd)) > eps:
        raise ValueError("Lines are not parallel")

    return distance_point_to_line(c, a, b)


def polygon_perimeter(points: Sequence[Point], closed: bool = True) -> float:
    """
    Compute the polyline or polygon perimeter / total path length.

    Args:
        points: sequence of points
        closed: if True, also includes edge from last to first

    Returns:
        Total length.
    """
    n = len(points)
    if n <= 1:
        return 0.0

    total = 0.0

    for i in range(1, n):
        total += points[i - 1].distance_to(points[i])

    if closed and n >= 2:
        total += points[-1].distance_to(points[0])

    return total


def polygon_area_signed(points: Sequence[Point]) -> float:
    """
    Compute signed area of a polygon using the shoelace formula.

    Args:
        points: polygon vertices in order

    Returns:
        Signed area:
            positive -> counterclockwise ordering
            negative -> clockwise ordering
            zero     -> degenerate polygon

    Notes:
        Requires at least 3 points for a non-zero area.
    """
    n = len(points)
    if n < 3:
        return 0.0

    area2 = 0.0
    for i in range(n):
        j = (i + 1) % n
        area2 += points[i].x * points[j].y
        area2 -= points[j].x * points[i].y

    return area2 / 2.0


def polygon_area(points: Sequence[Point]) -> float:
    """
    Absolute polygon area.
    """
    return abs(polygon_area_signed(points))


def is_polygon_clockwise(points: Sequence[Point]) -> bool:
    """
    Check whether polygon vertices are given in clockwise order.
    """
    return polygon_area_signed(points) < 0.0


def is_polygon_counterclockwise(points: Sequence[Point]) -> bool:
    """
    Check whether polygon vertices are given in counterclockwise order.
    """
    return polygon_area_signed(points) > 0.0


def bounding_box(points: Sequence[Point]) -> Tuple[Point, Point]:
    """
    Compute the axis-aligned bounding box of a non-empty set of points.

    Returns:
        (bottom_left, top_right)
    """
    if not points:
        raise ValueError("bounding_box requires at least one point")

    min_x = min(p.x for p in points)
    min_y = min(p.y for p in points)
    max_x = max(p.x for p in points)
    max_y = max(p.y for p in points)

    return Point(min_x, min_y), Point(max_x, max_y)


def closest_pair_bruteforce(points: Sequence[Point]) -> Optional[Tuple[Point, Point, float]]:
    """
    Brute-force closest pair of points.

    Args:
        points: sequence of points

    Returns:
        (point1, point2, distance), or None if fewer than 2 points

    Time Complexity:
        O(n^2)

    Notes:
        This is not the optimal closest-pair algorithm. It is intentionally
        simple and educational.
    """
    n = len(points)
    if n < 2:
        return None

    best_pair: Optional[Tuple[Point, Point, float]] = None
    best_distance = inf

    for i in range(n):
        for j in range(i + 1, n):
            dist = points[i].distance_to(points[j])
            if dist < best_distance:
                best_distance = dist
                best_pair = (points[i], points[j], dist)

    return best_pair


def segment_length(a: Point, b: Point) -> float:
    """
    Length of segment AB.
    """
    return a.distance_to(b)


def polyline_length(points: Sequence[Point]) -> float:
    """
    Total length of an open polyline.
    """
    return polygon_perimeter(points, closed=False)


def distance_between_segments(a: Point, b: Point, c: Point, d: Point) -> float:
    """
    Minimum distance between closed segments [a,b] and [c,d].

    If they intersect, the distance is 0.

    Strategy:
        If segments intersect -> 0
        Otherwise minimum of:
            dist(c, AB), dist(d, AB), dist(a, CD), dist(b, CD)
    """
    if segments_intersect(a, b, c, d):
        return 0.0

    return min(
        distance_point_to_segment(c, a, b),
        distance_point_to_segment(d, a, b),
        distance_point_to_segment(a, c, d),
        distance_point_to_segment(b, c, d),
    )


def explain_point_projections(p: Point, a: Point, b: Point) -> None:
    """
    Print projection and distance information for point p relative to line/ray/segment AB.
    """
    t = projection_parameter(p, a, b)
    proj = projection_point_on_line(p, a, b)

    print("\nProjection Demo")
    print("=" * 70)
    print(f"Point   : {p}")
    print(f"A       : {a}")
    print(f"B       : {b}")
    print("-" * 70)
    print(f"Projection parameter t     = {t}")
    print(f"Projection on line         = {proj}")
    print(f"Distance to line           = {distance_point_to_line(p, a, b)}")
    print(f"Distance to ray            = {distance_point_to_ray(p, a, b)}")
    print(f"Distance to segment        = {distance_point_to_segment(p, a, b)}")

    if t < 0:
        print("Projection lies before A")
    elif t > 1:
        print("Projection lies beyond B")
    else:
        print("Projection lies on segment AB")


def explain_polygon_properties(points: Sequence[Point]) -> None:
    """
    Print area, perimeter, orientation, and bounding box information for a polygon.
    """
    print("\nPolygon Properties Demo")
    print("=" * 70)
    print(f"Points               = {list(points)}")
    print("-" * 70)
    print(f"Signed area          = {polygon_area_signed(points)}")
    print(f"Absolute area        = {polygon_area(points)}")
    print(f"Perimeter            = {polygon_perimeter(points)}")
    print(f"Clockwise?           = {is_polygon_clockwise(points)}")
    print(f"Counterclockwise?    = {is_polygon_counterclockwise(points)}")
    box_min, box_max = bounding_box(points)
    print(f"Bounding box         = {box_min} -> {box_max}")


def explain_closest_pair(points: Sequence[Point]) -> None:
    """
    Print the brute-force closest pair of points.
    """
    result = closest_pair_bruteforce(points)

    print("\nClosest Pair Demo")
    print("=" * 70)
    print(f"Points = {list(points)}")
    print("-" * 70)

    if result is None:
        print("Need at least two points.")
        return

    p1, p2, dist = result
    print(f"Closest pair = {p1}, {p2}")
    print(f"Distance     = {dist}")


if __name__ == "__main__":
    print("Geometry Distances Demo")
    print("=" * 70)

    p = Point(2, 3)
    a = Point(0, 0)
    b = Point(4, 0)
    explain_point_projections(p, a, b)

    q = Point(-2, 1)
    explain_point_projections(q, a, b)

    polygon = [
        Point(0, 0),
        Point(4, 0),
        Point(4, 3),
        Point(0, 3),
    ]
    explain_polygon_properties(polygon)

    print("\nSegment Distance Demo")
    print("=" * 70)
    s1_a = Point(0, 0)
    s1_b = Point(2, 0)
    s2_a = Point(3, 1)
    s2_b = Point(3, 4)
    print(f"Distance between segments = {distance_between_segments(s1_a, s1_b, s2_a, s2_b)}")

    print("\nParallel Lines Demo")
    print("=" * 70)
    l1_a = Point(0, 0)
    l1_b = Point(4, 0)
    l2_a = Point(0, 3)
    l2_b = Point(5, 3)
    print(f"Distance between parallel lines = {distance_between_parallel_lines(l1_a, l1_b, l2_a, l2_b)}")

    sample_points = [
        Point(0, 0),
        Point(2, 2),
        Point(2.5, 2.2),
        Point(10, 10),
        Point(3, 3),
    ]
    explain_closest_pair(sample_points)

    print("\nSimple helpers")
    print("=" * 70)
    print(f"Segment length AB    = {segment_length(a, b)}")
    print(f"Polyline length      = {polyline_length([Point(0, 0), Point(1, 1), Point(4, 1)])}")

    line = line_from_points(Point(0, 0), Point(2, 2))
    test_point = Point(3, 3)
    print(f"Point {test_point} on line through (0,0)-(2,2)? {point_on_line(test_point, Point(0, 0), Point(2, 2))}")
    print(f"Line representation  = {line}")
