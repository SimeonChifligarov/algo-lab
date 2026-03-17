"""
Kruskal's Algorithm for finding a Minimum Spanning Tree (MST)
in a weighted, undirected graph.

Key ideas:
- Sort all edges by weight
- Repeatedly take the lightest edge that does not form a cycle
- Use Union-Find to efficiently detect cycles

This file depends on:
    from union_find import UnionFind
"""

from union_find import UnionFind


def kruskal_mst(num_vertices: int, edges: list[tuple[int, int, int]]) -> tuple[list[tuple[int, int, int]], int]:
    """
    Compute the Minimum Spanning Tree (MST) of a weighted undirected graph.

    Args:
        num_vertices:
            Number of vertices, assumed to be labeled 0..num_vertices-1

        edges:
            List of edges in the form (weight, u, v)

    Returns:
        A tuple:
            (mst_edges, total_weight)

        where:
            mst_edges is a list of edges chosen for the MST
            total_weight is the sum of their weights

    Raises:
        ValueError:
            If the graph is disconnected, so no spanning tree exists
    """
    if num_vertices <= 0:
        raise ValueError("num_vertices must be positive")

    uf = UnionFind(num_vertices)
    mst_edges: list[tuple[int, int, int]] = []
    total_weight = 0

    # Greedy step: consider edges from smallest weight to largest
    sorted_edges = sorted(edges)

    for weight, u, v in sorted_edges:
        _validate_vertex(u, num_vertices)
        _validate_vertex(v, num_vertices)

        # If u and v are in different components, adding this edge
        # will not create a cycle
        if uf.union(u, v):
            mst_edges.append((weight, u, v))
            total_weight += weight

            # Early stop: an MST for n vertices has exactly n - 1 edges
            if len(mst_edges) == num_vertices - 1:
                break

    if len(mst_edges) != num_vertices - 1:
        raise ValueError("graph is disconnected, so no MST exists")

    return mst_edges, total_weight


def _validate_vertex(vertex: int, num_vertices: int) -> None:
    if not 0 <= vertex < num_vertices:
        raise IndexError(f"vertex {vertex} is out of bounds for graph with {num_vertices} vertices")


def print_mst_result(mst_edges: list[tuple[int, int, int]], total_weight: int) -> None:
    """
    Nicely print the MST result.
    """
    print("Edges in MST:")
    for weight, u, v in mst_edges:
        print(f"  {u} -- {v}  (weight={weight})")
    print("Total MST weight:", total_weight)


def demo() -> None:
    print("=== Kruskal MST Demo ===")

    # Graph with 6 vertices: 0, 1, 2, 3, 4, 5
    #
    # Edge format: (weight, u, v)
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

    num_vertices = 6

    mst_edges, total_weight = kruskal_mst(num_vertices, edges)
    print_mst_result(mst_edges, total_weight)


if __name__ == "__main__":
    demo()
