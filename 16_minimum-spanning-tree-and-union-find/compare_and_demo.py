"""
compare_and_demo.py

A small demo / driver file that ties everything together:
- builds a sample weighted undirected graph
- runs Kruskal's algorithm
- runs Prim's algorithm
- compares the results
- shows a simple cycle-detection example with Union-Find

Expected files in the same folder:
- union_find.py
- kruskal_mst.py
- prim_mst.py
"""

from union_find import UnionFind
from kruskal_mst import kruskal_mst
from prim_mst import prim_mst


def print_graph(edges: list[tuple[int, int, int]]) -> None:
    """
    Print the graph edges in a readable way.
    Edge format: (weight, u, v)
    """
    print("Graph edges:")
    for weight, u, v in edges:
        print(f"  {u} -- {v}  (weight={weight})")
    print()


def print_mst(title: str, mst_edges: list[tuple[int, int, int]], total_weight: int) -> None:
    """
    Print an MST result in a readable way.
    """
    print(title)
    for weight, u, v in mst_edges:
        print(f"  {u} -- {v}  (weight={weight})")
    print(f"Total weight: {total_weight}")
    print()


def compare_mst_results(
        kruskal_result: tuple[list[tuple[int, int, int]], int],
        prim_result: tuple[list[tuple[int, int, int]], int],
) -> None:
    """
    Compare the outputs of Kruskal and Prim.

    Note:
    The exact chosen edges may differ when multiple valid MSTs exist
    with the same total weight. The most important comparison is the
    total weight and the number of edges.
    """
    kruskal_edges, kruskal_weight = kruskal_result
    prim_edges, prim_weight = prim_result

    print("=== Comparison ===")
    print(f"Kruskal edge count: {len(kruskal_edges)}")
    print(f"Prim edge count:    {len(prim_edges)}")
    print(f"Kruskal weight:     {kruskal_weight}")
    print(f"Prim weight:        {prim_weight}")

    if kruskal_weight == prim_weight and len(kruskal_edges) == len(prim_edges):
        print("Result: Both algorithms produced valid MST results with the same total weight.")
    else:
        print("Result: The outputs differ. Investigate the implementation or the input graph.")
    print()


def union_find_cycle_demo(num_vertices: int, edges: list[tuple[int, int, int]]) -> None:
    """
    Demonstrate simple cycle detection using Union-Find.

    Idea:
    - Process edges one by one
    - If an edge connects two vertices already in the same set,
      then that edge would create a cycle
    """
    print("=== Union-Find Cycle Detection Demo ===")

    uf = UnionFind(num_vertices)

    for weight, u, v in edges:
        if uf.connected(u, v):
            print(f"Adding edge {u} -- {v} (weight={weight}) would create a cycle.")
        else:
            uf.union(u, v)
            print(f"Added edge {u} -- {v} (weight={weight}); no cycle created.")

    print()
    print("Final groups:", uf.groups())
    print()


def main() -> None:
    # Sample weighted undirected graph
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

    print("=== Minimum Spanning Tree Demo ===")
    print()
    print_graph(edges)

    kruskal_edges, kruskal_weight = kruskal_mst(num_vertices, edges)
    prim_edges, prim_weight = prim_mst(num_vertices, edges, start=0)

    print_mst("=== Kruskal MST ===", kruskal_edges, kruskal_weight)
    print_mst("=== Prim MST ===", prim_edges, prim_weight)

    compare_mst_results(
        (kruskal_edges, kruskal_weight),
        (prim_edges, prim_weight),
    )

    union_find_cycle_demo(num_vertices, edges)


if __name__ == "__main__":
    main()
