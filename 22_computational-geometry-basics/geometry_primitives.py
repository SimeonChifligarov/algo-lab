"""
Fundamental geometry primitives and helper operations.

This file starts the computational geometry sequence with:
- a Point data class
- vector-style point operations
- dot product and cross product
- distance computations
- a robust orientation test
- floating-point comparison helpers

This is the base for later files such as segment intersection
and convex hull algorithms.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import hypot, sqrt, isclose
from typing import Iterable

EPSILON = 1e-9


def almost_equal(a: float, b: float, eps: float = EPSILON) -> bool:
    """
    Compare two floating-point values with a tolerance.

    Args:
        a: first number
        b: second number
        eps: absolute tolerance

    Returns:
        True if |a - b| <= eps, otherwise False
    """
    return abs(a - b) <= eps


@dataclass(frozen=True, order=True)
class Point:
    """
    2D point with basic vector-like operations.
    """
    x: float
    y: float

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Point":
        return Point(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Point":
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> "Point":
        if almost_equal(scalar, 0.0):
            raise ValueError("division by zero or near-zero scalar")
        return Point(self.x / scalar, self.y / scalar)

    def as_tuple(self) -> tuple[float, float]:
        """
        Return the point as a plain tuple.
        """
        return (self.x, self.y)

    def norm(self) -> float:
        """
        Return the Euclidean length of the vector from origin.
        """
        return hypot(self.x, self.y)

    def norm_squared(self) -> float:
        """
        Return squared Euclidean length.
        """
        return self.x * self.x + self.y * self.y

    def distance_to(self, other: "Point") -> float:
        """
        Euclidean distance to another point.
        """
        return hypot(self.x - other.x, self.y - other.y)

    def distance_squared_to(self, other: "Point") -> float:
        """
        Squared Euclidean distance to another point.
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return dx * dx + dy * dy


def dot(a: Point, b: Point) -> float:
    """
    Dot product of two vectors represented as points.
    """
    return a.x * b.x + a.y * b.y


def cross(a: Point, b: Point) -> float:
    """
    2D cross product of vectors a and b.

    Returns:
        Positive if b is to the left of a,
        negative if b is to the right,
        zero if they are parallel / collinear.
    """
    return a.x * b.y - a.y * b.x


def cross_three(a: Point, b: Point, c: Point) -> float:
    """
    Cross product of vectors AB and AC.

    Equivalent to:
        cross(b - a, c - a)

    Commonly used in orientation tests.
    """
    return cross(b - a, c - a)


def orientation(a: Point, b: Point, c: Point, eps: float = EPSILON) -> int:
    """
    Determine orientation of the triplet (a, b, c).

    Args:
        a, b, c: points
        eps: tolerance for collinearity

    Returns:
        +1 if counterclockwise
        -1 if clockwise
         0 if collinear

    Interpretation:
        sign of cross((b - a), (c - a))
    """
    value = cross_three(a, b, c)

    if value > eps:
        return 1
    if value < -eps:
        return -1
    return 0


def orientation_name(a: Point, b: Point, c: Point, eps: float = EPSILON) -> str:
    """
    Human-readable orientation result.
    """
    result = orientation(a, b, c, eps)
    if result == 1:
        return "counterclockwise"
    if result == -1:
        return "clockwise"
    return "collinear"


def midpoint(a: Point, b: Point) -> Point:
    """
    Midpoint of segment AB.
    """
    return Point((a.x + b.x) / 2.0, (a.y + b.y) / 2.0)


def triangle_area_signed(a: Point, b: Point, c: Point) -> float:
    """
    Signed area of triangle ABC.

    Positive -> counterclockwise
    Negative -> clockwise
    Zero     -> collinear
    """
    return cross_three(a, b, c) / 2.0


def triangle_area(a: Point, b: Point, c: Point) -> float:
    """
    Absolute area of triangle ABC.
    """
    return abs(triangle_area_signed(a, b, c))


def are_collinear(a: Point, b: Point, c: Point, eps: float = EPSILON) -> bool:
    """
    Check whether three points are collinear.
    """
    return orientation(a, b, c, eps) == 0


def distance_between_points(a: Point, b: Point) -> float:
    """
    Euclidean distance between two points.
    """
    return a.distance_to(b)


def manhattan_distance(a: Point, b: Point) -> float:
    """
    Manhattan (L1) distance between two points.
    """
    return abs(a.x - b.x) + abs(a.y - b.y)


def chebyshev_distance(a: Point, b: Point) -> float:
    """
    Chebyshev (L-infinity) distance between two points.
    """
    return max(abs(a.x - b.x), abs(a.y - b.y))


def centroid(points: Iterable[Point]) -> Point:
    """
    Compute the centroid (arithmetic mean) of a non-empty set of points.
    """
    points = list(points)
    if not points:
        raise ValueError("centroid requires at least one point")

    sx = sum(p.x for p in points)
    sy = sum(p.y for p in points)
    return Point(sx / len(points), sy / len(points))


def explain_orientation(a: Point, b: Point, c: Point) -> None:
    """
    Print a compact explanation of the orientation test.
    """
    value = cross_three(a, b, c)

    print("\nOrientation Test")
    print("=" * 60)
    print(f"A = {a}")
    print(f"B = {b}")
    print(f"C = {c}")
    print("-" * 60)
    print(f"AB = {b - a}")
    print(f"AC = {c - a}")
    print(f"cross(AB, AC) = {value}")
    print(f"orientation = {orientation_name(a, b, c)}")


def explain_distances(a: Point, b: Point) -> None:
    """
    Print several common distance measures between two points.
    """
    print("\nDistance Demo")
    print("=" * 60)
    print(f"A = {a}")
    print(f"B = {b}")
    print("-" * 60)
    print(f"Euclidean distance       = {distance_between_points(a, b)}")
    print(f"Euclidean distance^2     = {a.distance_squared_to(b)}")
    print(f"Manhattan distance       = {manhattan_distance(a, b)}")
    print(f"Chebyshev distance       = {chebyshev_distance(a, b)}")
    print(f"Midpoint                 = {midpoint(a, b)}")


if __name__ == "__main__":
    p1 = Point(0, 0)
    p2 = Point(4, 0)
    p3 = Point(2, 3)
    p4 = Point(2, -3)
    p5 = Point(2, 0)

    print("Geometry Primitives Demo")
    print("=" * 60)

    explain_orientation(p1, p2, p3)
    explain_orientation(p1, p2, p4)
    explain_orientation(p1, p2, p5)

    explain_distances(Point(1, 2), Point(4, 6))

    print("\nVector Operations")
    print("=" * 60)
    a = Point(3, 4)
    b = Point(1, -2)
    print(f"a                  = {a}")
    print(f"b                  = {b}")
    print(f"a + b              = {a + b}")
    print(f"a - b              = {a - b}")
    print(f"2 * a              = {2 * a}")
    print(f"dot(a, b)          = {dot(a, b)}")
    print(f"cross(a, b)        = {cross(a, b)}")
    print(f"|a|                = {a.norm()}")
    print(f"|a|^2              = {a.norm_squared()}")

    print("\nTriangle Area")
    print("=" * 60)
    print(f"signed area        = {triangle_area_signed(p1, p2, p3)}")
    print(f"absolute area      = {triangle_area(p1, p2, p3)}")

    pts = [Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)]
    print("\nCentroid")
    print("=" * 60)
    print(f"points             = {pts}")
    print(f"centroid           = {centroid(pts)}")
