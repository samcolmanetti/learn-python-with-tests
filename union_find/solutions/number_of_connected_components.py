from __future__ import annotations

from .._template import UnionFind


def count_components(n: int, edges: list[list[int]]) -> int:
    uf = UnionFind()
    for node in range(n):
        uf.find(node)
    for a, b in edges:
        uf.union(a, b)
    return uf.count
