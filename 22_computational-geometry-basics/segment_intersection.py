"""
Line and segment geometry with a focus on intersection tests.

This module builds on basic geometry primitives and covers:
- line equation helpers
- checking whether a point lies on a segment
- segment intersection test
- segment intersection classification
- computing the actual intersection point for non-parallel lines
- distance from a point to a line / segment

This is one of the most important basic topics in computational geometry,
because many larger problems reduce to robust orientation and intersection logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Optional

from geometry_primitives import (
    EPSILON,
    Point,
    almost_equal,
    cross,
    cross_three,
    dot,
    orientation,
    orientation_name,
)


@dataclass(frozen=True)
class Line:
    """
    2D line in the form:
        a*x + b*y + c = 0

    This representation is useful for line intersection and distance formulas.
    """
    a: float
    b: float
    c: float

    def evaluate(self, p: Point) -> float:
        """
        Evaluate a*x + b*y + c at a point.
        """
        return self.a * p.x + self.b * p.y + self.c

    def normalized(self) -> "Line":
        """
        Return an equivalent line scaled so that sqrt(a^2 + b^2) = 1.

        Raises:
            ValueError: if the line coefficients are degenerate
        """
        norm = sqrt(self.a * self.a + self.b * self.b)
        if almost_equal(norm, 0.0):
            raise ValueError("Cannot normalize a degenerate line")
        return Line(self.a / norm, self.b / norm, self.c / norm)


def line_from_points(a: Point, b: Point) -> Line:
    """
    Construct the line passing through points a and b.

    Raises:
        ValueError: if a and b are the same point
    """
    if almost_equal(a.x, b.x) and almost_equal(a.y, b.y):
        raise ValueError("A line requires two distinct points")

    A = a.y - b.y
    B = b.x - a.x
    C = a.x * b.y - b.x * a.y
    return Line(A, B, C)


def point_on_line(p: Point, a: Point, b: Point, eps: float = EPSILON) -> bool:
    """
    Check whether point p lies on the infinite line through a and b.
    """
    return abs(cross_three(a, b, p)) <= eps


def point_on_segment(p: Point, a: Point, b: Point, eps: float = EPSILON) -> bool:
    """
    Check whether point p lies on the closed segment [a, b].

    Conditions:
        1) p is collinear with a and b
        2) p lies within the axis-aligned bounding box of the segment
    """
    if orientation(a, b, p, eps) != 0:
        return False

    return (
            min(a.x, b.x) - eps <= p.x <= max(a.x, b.x) + eps
            and min(a.y, b.y) - eps <= p.y <= max(a.y, b.y) + eps
    )


def bounding_boxes_overlap(a: Point, b: Point, c: Point, d: Point, eps: float = EPSILON) -> bool:
    """
    Fast bounding-box overlap check for segments [a,b] and [c,d].
    """
    return (
            max(min(a.x, b.x), min(c.x, d.x)) <= min(max(a.x, b.x), max(c.x, d.x)) + eps
            and max(min(a.y, b.y), min(c.y, d.y)) <= min(max(a.y, b.y), max(c.y, d.y)) + eps
    )


def segments_intersect(a: Point, b: Point, c: Point, d: Point, eps: float = EPSILON) -> bool:
    """
    Check whether closed segments [a,b] and [c,d] intersect.

    Handles:
        - proper intersections
        - endpoint touching
        - collinear overlap
        - degenerate point-segments
    """
    o1 = orientation(a, b, c, eps)
    o2 = orientation(a, b, d, eps)
    o3 = orientation(c, d, a, eps)
    o4 = orientation(c, d, b, eps)

    # Proper intersection
    if o1 != o2 and o3 != o4:
        return True

    # Special collinear / touching cases
    if o1 == 0 and point_on_segment(c, a, b, eps):
        return True
    if o2 == 0 and point_on_segment(d, a, b, eps):
        return True
    if o3 == 0 and point_on_segment(a, c, d, eps):
        return True
    if o4 == 0 and point_on_segment(b, c, d, eps):
        return True

    return False


def segment_intersection_type(a: Point, b: Point, c: Point, d: Point, eps: float = EPSILON) -> str:
    """
    Classify the relationship between two closed segments.

    Returns one of:
        - "none"
        - "proper"
        - "touching"
        - "overlapping"

    Notes:
        - "proper" means interiors cross at a single point
        - "touching" means they meet at an endpoint or one point only
        - "overlapping" means collinear and share more than one point
    """
    if not segments_intersect(a, b, c, d, eps):
        return "none"

    o1 = orientation(a, b, c, eps)
    o2 = orientation(a, b, d, eps)
    o3 = orientation(c, d, a, eps)
    o4 = orientation(c, d, b, eps)

    if o1 == 0 and o2 == 0 and o3 == 0 and o4 == 0:
        # Collinear case: determine whether overlap is only a point or a segment
        points = [a, b, c, d]
        points_sorted_x = sorted(points, key=lambda p: (p.x, p.y))
        points_sorted_y = sorted(points, key=lambda p: (p.y, p.x))

        if almost_equal(a.x, b.x) and almost_equal(c.x, d.x):
            left = points_sorted_y[1]
            right = points_sorted_y[2]
        else:
            left = points_sorted_x[1]
            right = points_sorted_x[2]

        if left == right:
            return "touching"
        return "overlapping"

    # Endpoint / collinear touching
    if (
            (o1 == 0 and point_on_segment(c, a, b, eps))
            or (o2 == 0 and point_on_segment(d, a, b, eps))
            or (o3 == 0 and point_on_segment(a, c, d, eps))
            or (o4 == 0 and point_on_segment(b, c, d, eps))
    ):
        return "touching"

    return "proper"


def line_intersection(a: Point, b: Point, c: Point, d: Point, eps: float = EPSILON) -> Optional[Point]:
    """
    Compute the intersection point of the infinite lines AB and CD.

    Returns:
        Point of intersection, or None if the lines are parallel
        (including coincident lines).

    Notes:
        This is line-line intersection, not segment-segment intersection.
    """
    ab = b - a
    cd = d - c
    denominator = cross(ab, cd)

    if abs(denominator) <= eps:
        return None

    t = cross(c - a, cd) / denominator
    return a + ab * t


def segment_intersection_point(
        a: Point,
        b: Point,
        c: Point,
        d: Point,
        eps: float = EPSILON,
) -> Optional[Point]:
    """
    Return the unique intersection point of segments [a,b] and [c,d], if it exists.

    Returns:
        - Point if there is exactly one intersection point
        - None if there is no intersection or infinitely many intersection points
          (overlapping collinear segments)
    """
    kind = segment_intersection_type(a, b, c, d, eps)

    if kind == "none":
        return None

    if kind == "overlapping":
        return None

    if orientation(a, b, c, eps) == 0 and point_on_segment(c, a, b, eps):
        return c
    if orientation(a, b, d, eps) == 0 and point_on_segment(d, a, b, eps):
        return d
    if orientation(c, d, a, eps) == 0 and point_on_segment(a, c, d, eps):
        return a
    if orientation(c, d, b, eps) == 0 and point_on_segment(b, c, d, eps):
        return b

    return line_intersection(a, b, c, d, eps)


def distance_point_to_line(p: Point, a: Point, b: Point) -> float:
    """
    Distance from point p to the infinite line through a and b.

    Raises:
        ValueError: if a and b are the same point
    """
    ab = b - a
    if almost_equal(ab.x, 0.0) and almost_equal(ab.y, 0.0):
        raise ValueError("Line requires two distinct points")

    return abs(cross(p - a, ab)) / sqrt(dot(ab, ab))


def distance_point_to_segment(p: Point, a: Point, b: Point) -> float:
    """
    Distance from point p to the closed segment [a,b].

    Handles projection onto the segment interior or nearest endpoint.
    """
    ab = b - a
    ap = p - a
    bp = p - b

    ab_len_sq = dot(ab, ab)
    if almost_equal(ab_len_sq, 0.0):
        return p.distance_to(a)

    t = dot(ap, ab) / ab_len_sq

    if t < 0.0:
        return p.distance_to(a)
    if t > 1.0:
        return p.distance_to(b)

    projection = a + ab * t
    return p.distance_to(projection)


def explain_segment_intersection(a: Point, b: Point, c: Point, d: Point) -> None:
    """
    Print a compact explanation of segment intersection logic.
    """
    o1 = orientation(a, b, c)
    o2 = orientation(a, b, d)
    o3 = orientation(c, d, a)
    o4 = orientation(c, d, b)

    print("\nSegment Intersection Demo")
    print("=" * 70)
    print(f"Segment 1: {a} -> {b}")
    print(f"Segment 2: {c} -> {d}")
    print("-" * 70)
    print(f"orientation(a, b, c) = {o1} ({orientation_name(a, b, c)})")
    print(f"orientation(a, b, d) = {o2} ({orientation_name(a, b, d)})")
    print(f"orientation(c, d, a) = {o3} ({orientation_name(c, d, a)})")
    print(f"orientation(c, d, b) = {o4} ({orientation_name(c, d, b)})")
    print("-" * 70)
    print(f"bounding boxes overlap  = {bounding_boxes_overlap(a, b, c, d)}")
    print(f"segments intersect      = {segments_intersect(a, b, c, d)}")
    print(f"intersection type       = {segment_intersection_type(a, b, c, d)}")
    print(f"unique intersection pt  = {segment_intersection_point(a, b, c, d)}")


def explain_distances_to_segment(p: Point, a: Point, b: Point) -> None:
    """
    Print distances from point p to the line AB and segment AB.
    """
    print("\nPoint-to-Line / Segment Distance Demo")
    print("=" * 70)
    print(f"Point   : {p}")
    print(f"Segment : {a} -> {b}")
    print("-" * 70)
    print(f"Distance to infinite line = {distance_point_to_line(p, a, b)}")
    print(f"Distance to segment       = {distance_point_to_segment(p, a, b)}")


if __name__ == "__main__":
    print("Segment Geometry Demo")
    print("=" * 70)

    s1_a = Point(0, 0)
    s1_b = Point(4, 4)
    s2_a = Point(0, 4)
    s2_b = Point(4, 0)
    explain_segment_intersection(s1_a, s1_b, s2_a, s2_b)

    t1_a = Point(0, 0)
    t1_b = Point(4, 0)
    t2_a = Point(4, 0)
    t2_b = Point(6, 2)
    explain_segment_intersection(t1_a, t1_b, t2_a, t2_b)

    u1_a = Point(0, 0)
    u1_b = Point(6, 0)
    u2_a = Point(2, 0)
    u2_b = Point(4, 0)
    explain_segment_intersection(u1_a, u1_b, u2_a, u2_b)

    v1_a = Point(0, 0)
    v1_b = Point(2, 2)
    v2_a = Point(3, 3)
    v2_b = Point(5, 5)
    explain_segment_intersection(v1_a, v1_b, v2_a, v2_b)

    explain_distances_to_segment(Point(2, 3), Point(0, 0), Point(4, 0))
    explain_distances_to_segment(Point(-1, 2), Point(0, 0), Point(4, 0))
