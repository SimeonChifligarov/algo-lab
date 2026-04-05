"""
Convex hull algorithms and helpers.

This module completes the computational geometry basics sequence with:
- convex hull using the Monotonic Chain algorithm
- optional handling of collinear boundary points
- polygon convexity check
- point-in-convex-polygon helper (boundary-inclusive, linear scan)
- hull area and perimeter helpers
- demonstrations of common edge cases

Why convex hull?
    The convex hull of a set of points is the smallest convex polygon
    containing all of them. It is one of the most fundamental structures
    in computational geometry.

Main algorithm here:
    Andrew's Monotonic Chain
    - sort points
    - build lower hull
    - build upper hull
    - combine them

Time complexity:
    O(n log n) due to sorting
"""

from __future__ import annotations

from typing import Iterable, List, Sequence

from geometry_primitives import (
    EPSILON,
    Point,
    orientation,
)
from geometry_distances import polygon_area, polygon_perimeter
from segment_intersection import point_on_segment


def _unique_sorted_points(points: Iterable[Point]) -> List[Point]:
    """
    Return points sorted lexicographically with duplicates removed.
    """
    return sorted(set(points))


def _should_pop(
        a: Point,
        b: Point,
        c: Point,
        include_collinear_boundary: bool,
) -> bool:
    """
    Decide whether the middle point b should be removed while building the hull.

    For strict hull vertices only:
        pop on clockwise or collinear turns  -> orientation <= 0

    For including all boundary-collinear points:
        pop only on clockwise turns          -> orientation < 0
    """
    turn = orientation(a, b, c)

    if include_collinear_boundary:
        return turn < 0
    return turn <= 0


def convex_hull(points: Sequence[Point], include_collinear_boundary: bool = False) -> List[Point]:
    """
    Compute the convex hull using Andrew's Monotonic Chain algorithm.

    Args:
        points: input points
        include_collinear_boundary:
            - False: keep only extreme hull vertices
            - True: include collinear points that lie on hull edges

    Returns:
        List of hull points in counterclockwise order, without repeating
        the first point at the end.

    Edge cases:
        - 0 points -> []
        - 1 point  -> [p]
        - all points collinear:
            * False -> just the two endpoints (or one point if identical)
            * True  -> all unique points in sorted order, then reversed path
                       logic is handled naturally by the algorithm and post-fix
    """
    pts = _unique_sorted_points(points)

    if len(pts) <= 1:
        return pts[:]

    lower: List[Point] = []
    for p in pts:
        while len(lower) >= 2 and _should_pop(
                lower[-2],
                lower[-1],
                p,
                include_collinear_boundary,
        ):
            lower.pop()
        lower.append(p)

    upper: List[Point] = []
    for p in reversed(pts):
        while len(upper) >= 2 and _should_pop(
                upper[-2],
                upper[-1],
                p,
                include_collinear_boundary,
        ):
            upper.pop()
        upper.append(p)

    hull = lower[:-1] + upper[:-1]

    if not include_collinear_boundary:
        return hull

    # For all-collinear inputs, the simple lower/upper concatenation duplicates
    # interior points in a mirrored walk. In that special case, return unique sorted.
    if len(hull) > 1 and all(orientation(hull[0], hull[-1], p) == 0 for p in hull):
        return pts

    # Remove accidental duplicates while preserving order.
    cleaned: List[Point] = []
    seen = set()
    for p in hull:
        if p not in seen:
            cleaned.append(p)
            seen.add(p)

    return cleaned


def convex_hull_vertices_only(points: Sequence[Point]) -> List[Point]:
    """
    Convenience wrapper: convex hull with only the extreme corner vertices.
    """
    return convex_hull(points, include_collinear_boundary=False)


def convex_hull_with_boundary_points(points: Sequence[Point]) -> List[Point]:
    """
    Convenience wrapper: convex hull including collinear boundary points.
    """
    return convex_hull(points, include_collinear_boundary=True)


def is_convex_polygon(points: Sequence[Point], strict: bool = False) -> bool:
    """
    Check whether a polygon is convex.

    Args:
        points: polygon vertices in order
        strict:
            - False: allows collinear edges
            - True: requires every turn to be strictly left or strictly right

    Returns:
        True if the polygon is convex under the chosen interpretation.

    Notes:
        This assumes the polygon boundary is given in order and is simple.
    """
    n = len(points)
    if n < 3:
        return False

    direction = 0

    for i in range(n):
        a = points[i]
        b = points[(i + 1) % n]
        c = points[(i + 2) % n]

        turn = orientation(a, b, c)

        if turn == 0:
            if strict:
                return False
            continue

        if direction == 0:
            direction = turn
        elif turn != direction:
            return False

    return True


def point_in_convex_polygon(point: Point, polygon: Sequence[Point], eps: float = EPSILON) -> bool:
    """
    Check whether a point lies inside or on the boundary of a convex polygon.

    Args:
        point: query point
        polygon: convex polygon vertices in clockwise or counterclockwise order
        eps: tolerance

    Returns:
        True if point is inside or on boundary, else False

    Notes:
        This is a simple O(n) method based on consistent orientation.
        Good for learning and small inputs.
    """
    n = len(polygon)

    if n == 0:
        return False
    if n == 1:
        return point == polygon[0]
    if n == 2:
        return point_on_segment(point, polygon[0], polygon[1], eps)

    sign = 0

    for i in range(n):
        a = polygon[i]
        b = polygon[(i + 1) % n]

        turn = orientation(a, b, point, eps)

        if turn == 0 and point_on_segment(point, a, b, eps):
            return True

        if turn == 0:
            continue

        if sign == 0:
            sign = turn
        elif turn != sign:
            return False

    return True


def hull_area(points: Sequence[Point], include_collinear_boundary: bool = False) -> float:
    """
    Compute area of the convex hull of a point set.
    """
    hull = convex_hull(points, include_collinear_boundary=include_collinear_boundary)
    return polygon_area(hull)


def hull_perimeter(points: Sequence[Point], include_collinear_boundary: bool = False) -> float:
    """
    Compute perimeter of the convex hull of a point set.
    """
    hull = convex_hull(points, include_collinear_boundary=include_collinear_boundary)

    if len(hull) == 0:
        return 0.0
    if len(hull) == 1:
        return 0.0
    if len(hull) == 2:
        return 2.0 * hull[0].distance_to(hull[1])

    return polygon_perimeter(hull, closed=True)


def extreme_points(points: Sequence[Point]) -> List[Point]:
    """
    Return the extreme corner vertices of the convex hull.
    """
    return convex_hull_vertices_only(points)


def hull_edges(hull: Sequence[Point]) -> List[tuple[Point, Point]]:
    """
    Return the directed edges of a hull/polygon.

    For fewer than 2 points:
        returns []
    For 2 points:
        returns [(p0, p1)]
    For 3+ points:
        returns cyclic edges
    """
    n = len(hull)

    if n < 2:
        return []
    if n == 2:
        return [(hull[0], hull[1])]

    return [(hull[i], hull[(i + 1) % n]) for i in range(n)]


def explain_convex_hull(points: Sequence[Point], include_collinear_boundary: bool = False) -> None:
    """
    Print the input points and resulting convex hull.
    """
    hull = convex_hull(points, include_collinear_boundary=include_collinear_boundary)

    print("\nConvex Hull Demo")
    print("=" * 70)
    print(f"Input points ({len(points)}):")
    for p in points:
        print(f"  {p}")

    print("-" * 70)
    print(
        "Mode: "
        + (
            "include boundary-collinear points"
            if include_collinear_boundary
            else "vertices only"
        )
    )
    print(f"Hull ({len(hull)} points):")
    for p in hull:
        print(f"  {p}")

    print("-" * 70)
    print(f"Hull area      = {polygon_area(hull)}")
    if len(hull) == 2:
        print(f"Hull perimeter = {2.0 * hull[0].distance_to(hull[1])}")
    else:
        print(f"Hull perimeter = {polygon_perimeter(hull, closed=True) if len(hull) >= 3 else 0.0}")
    print(f"Is convex?     = {is_convex_polygon(hull, strict=False) if len(hull) >= 3 else True}")


def explain_point_membership(point: Point, polygon: Sequence[Point]) -> None:
    """
    Print whether a point lies inside a convex polygon.
    """
    print("\nPoint in Convex Polygon Demo")
    print("=" * 70)
    print(f"Point   : {point}")
    print(f"Polygon : {list(polygon)}")
    print("-" * 70)
    print(f"Inside or on boundary? -> {point_in_convex_polygon(point, polygon)}")


if __name__ == "__main__":
    print("Convex Hull Demo")
    print("=" * 70)

    sample_points = [
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

    explain_convex_hull(sample_points, include_collinear_boundary=False)
    explain_convex_hull(sample_points, include_collinear_boundary=True)

    print("\nConvenience Helpers")
    print("=" * 70)
    hull = convex_hull_vertices_only(sample_points)
    print(f"Extreme points         = {extreme_points(sample_points)}")
    print(f"Hull edges             = {hull_edges(hull)}")
    print(f"Hull area              = {hull_area(sample_points)}")
    print(f"Hull perimeter         = {hull_perimeter(sample_points)}")

    print("\nAll-Collinear Example")
    print("=" * 70)
    collinear_points = [
        Point(0, 0),
        Point(1, 0),
        Point(2, 0),
        Point(3, 0),
        Point(2, 0),
    ]
    print("Vertices only hull:")
    print(convex_hull_vertices_only(collinear_points))
    print("Hull with boundary points:")
    print(convex_hull_with_boundary_points(collinear_points))

    print("\nConvexity Check")
    print("=" * 70)
    square = [Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)]
    non_convex = [Point(0, 0), Point(2, 0), Point(1, 1), Point(2, 2), Point(0, 2)]
    print(f"Square convex?         = {is_convex_polygon(square)}")
    print(f"Non-convex polygon?    = {is_convex_polygon(non_convex)}")

    print("\nPoint Membership")
    print("=" * 70)
    hull_polygon = convex_hull_vertices_only(sample_points)
    explain_point_membership(Point(1, 1), hull_polygon)
    explain_point_membership(Point(3, 3), hull_polygon)
    explain_point_membership(Point(2, 0), hull_polygon)
