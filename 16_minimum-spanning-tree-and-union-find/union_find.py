"""
Disjoint Set Union (Union-Find) with:
- path compression
- union by rank

This structure is useful for:
- tracking connected components
- cycle detection
- Kruskal's Minimum Spanning Tree algorithm
"""


class UnionFind:
    def __init__(self, size: int):
        """
        Create 'size' disjoint sets: {0}, {1}, {2}, ..., {size-1}
        """
        if size <= 0:
            raise ValueError("size must be positive")

        self.parent = list(range(size))
        self.rank = [0] * size
        self.components = size

    def find(self, x: int) -> int:
        """
        Find the representative (root) of the set containing x.
        Uses path compression to flatten the tree.
        """
        self._validate(x)

        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, a: int, b: int) -> bool:
        """
        Merge the sets containing a and b.
        Returns True if a merge happened, False if they were already connected.

        Uses union by rank to keep trees shallow.
        """
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return False

        # Union by rank
        if self.rank[root_a] < self.rank[root_b]:
            self.parent[root_a] = root_b
        elif self.rank[root_a] > self.rank[root_b]:
            self.parent[root_b] = root_a
        else:
            self.parent[root_b] = root_a
            self.rank[root_a] += 1

        self.components -= 1
        return True

    def connected(self, a: int, b: int) -> bool:
        """
        Return True if a and b belong to the same set.
        """
        return self.find(a) == self.find(b)

    def count_components(self) -> int:
        """
        Return the current number of connected components.
        """
        return self.components

    def groups(self) -> dict[int, list[int]]:
        """
        Return the current partition as:
        {root: [members]}
        """
        result: dict[int, list[int]] = {}
        for node in range(len(self.parent)):
            root = self.find(node)
            if root not in result:
                result[root] = []
            result[root].append(node)
        return result

    def _validate(self, x: int) -> None:
        if not 0 <= x < len(self.parent):
            raise IndexError(f"node {x} is out of bounds for size {len(self.parent)}")


def demo() -> None:
    print("=== Union-Find Demo ===")

    uf = UnionFind(7)

    print("Initial components:", uf.count_components())
    print("Initial groups:", uf.groups())

    operations = [
        (0, 1),
        (1, 2),
        (3, 4),
        (5, 6),
        (2, 6),
        (0, 6),  # already connected by this point
    ]

    for a, b in operations:
        merged = uf.union(a, b)
        print(f"union({a}, {b}) -> {merged}")
        print("groups:", uf.groups())
        print("components:", uf.count_components())
        print()

    print("connected(0, 6):", uf.connected(0, 6))
    print("connected(3, 5):", uf.connected(3, 5))
    print("Final parent array:", uf.parent)
    print("Final rank array:", uf.rank)


if __name__ == "__main__":
    demo()
