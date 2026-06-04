"""Union Find (Disjoint Set Union) — near-O(1) "are these connected?" / "merge these".

Maintain a forest where each element points to a parent; the root identifies the set. Two
optimisations make operations effectively constant time:

- **Path compression**: ``find`` re-points nodes directly at the root as it climbs.
- **Union by rank**: ``union`` hangs the shorter tree under the taller one.

Use it for connectivity, counting connected components, cycle detection in an undirected
graph, and "accounts merge"-style grouping.
"""

from __future__ import annotations

from collections.abc import Hashable


class UnionFind:
    def __init__(self) -> None:
        self._parent: dict = {}
        self._rank: dict = {}
        self.count = 0  # number of disjoint sets

    def find(self, x: Hashable) -> Hashable:
        """Return the representative root of ``x`` (adding ``x`` as its own set if new)."""
        if x not in self._parent:
            self._parent[x] = x
            self._rank[x] = 0
            self.count += 1
        root = x
        while self._parent[root] != root:
            root = self._parent[root]
        while self._parent[x] != root:  # path compression
            self._parent[x], x = root, self._parent[x]
        return root

    def union(self, a: Hashable, b: Hashable) -> bool:
        """Merge the sets containing ``a`` and ``b``.

        Returns ``True`` if they were previously separate (a real merge happened), ``False``
        if they were already connected — handy for cycle detection.
        """
        root_a, root_b = self.find(a), self.find(b)
        if root_a == root_b:
            return False
        if self._rank[root_a] < self._rank[root_b]:
            root_a, root_b = root_b, root_a
        self._parent[root_b] = root_a
        if self._rank[root_a] == self._rank[root_b]:
            self._rank[root_a] += 1
        self.count -= 1
        return True

    def connected(self, a: Hashable, b: Hashable) -> bool:
        """Whether ``a`` and ``b`` are in the same set."""
        return self.find(a) == self.find(b)
