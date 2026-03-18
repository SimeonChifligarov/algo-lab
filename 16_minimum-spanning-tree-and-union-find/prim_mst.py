"""
Prim's Algorithm for finding a Minimum Spanning Tree (MST)
in a weighted, undirected graph.

Key ideas:
- Start from any vertex
- Grow the tree one edge at a time
- Always choose the minimum-weight edge that connects
  a visited vertex to an unvisited vertex
- Use a priority queue (min-heap) for efficiency
"""

import heapq


def build_adjacency_list(
        num_vertices: int,
        edges: list[tuple[int, int, int]],
) -> list[list[tuple[int, int]]]:
    """
    Build an adjacency list for an undirected weighted graph.

    Args:
        num_vertices:
            Number of vertices labeled 0..num_vertices-1

        edges:
            List of edges in the form (weight, u, v)

    Returns:
        adjacency list where adj[u] contains (neighbor, weight)
    """
    if num_vertices <= 0:
        raise ValueError("num_vertices must be positive")

    adj: list[list[tuple[int, int]]] = [[] for _ in range(num_vertices)]

    for weight, u, v in edges:
        _validate_vertex(u, num_vertices)
        _validate_vertex(v, num_vertices)

        adj[u].append((v, weight))
        adj[v].append((u, weight))

    return adj


def prim_mst(
        num_vertices: int,
        edges: list[tuple[int, int, int]],
        start: int = 0,
) -> tuple[list[tuple[int, int, int]], int]:
    """
    Compute the Minimum Spanning Tree (MST) using Prim's algorithm.

    Args:
        num_vertices:
            Number of vertices labeled 0..num_vertices-1

        edges:
            List of edges in the form (weight, u, v)

        start:
            Starting vertex for Prim's algorithm

    Returns:
        A tuple:
            (mst_edges, total_weight)

        mst_edges contains edges as (weight, u, v)
        total_weight is the sum of MST edge weights

    Raises:
        ValueError:
            If the graph is disconnected
    """
    if num_vertices <= 0:
        raise ValueError("num_vertices must be positive")

    _validate_vertex(start, num_vertices)

    adj = build_adjacency_list(num_vertices, edges)

    visited = [False] * num_vertices
    mst_edges: list[tuple[int, int, int]] = []
    total_weight = 0

    # Heap entries: (weight, from_vertex, to_vertex)
    min_heap: list[tuple[int, int, int]] = []

    def add_edges(vertex: int) -> None:
        """
        Mark vertex as visited and push all outgoing edges
        to unvisited neighbors into the heap.
        """
        visited[vertex] = True
        for neighbor, weight in adj[vertex]:
            if not visited[neighbor]:
                heapq.heappush(min_heap, (weight, vertex, neighbor))

    add_edges(start)

    while min_heap and len(mst_edges) < num_vertices - 1:
        weight, u, v = heapq.heappop(min_heap)

        if visited[v]:
            continue

        mst_edges.append((weight, u, v))
        total_weight += weight
        add_edges(v)

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
    print("=== Prim MST Demo ===")

    # Same example graph as in kruskal_mst.py
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

    mst_edges, total_weight = prim_mst(num_vertices, edges, start=0)
    print_mst_result(mst_edges, total_weight)


if __name__ == "__main__":
    demo()
