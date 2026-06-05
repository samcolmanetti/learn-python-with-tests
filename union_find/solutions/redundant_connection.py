from __future__ import annotations

from .._template import UnionFind


def find_redundant_connection(edges: list[list[int]]) -> list[int]:
    uf = UnionFind()
    for a, b in edges:
        if not uf.union(a, b):
            return [a, b]
    return []
