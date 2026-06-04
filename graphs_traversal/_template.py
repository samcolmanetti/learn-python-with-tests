"""Graph traversal — BFS and DFS on adjacency lists, plus matrix-as-graph neighbours.

The only thing that separates graph traversal from tree traversal is **cycles**: a graph can
revisit nodes, so you must track a ``visited`` set. With that one addition, BFS (queue) and
DFS (recursion or stack) carry straight over.

A grid is just an implicit graph: each cell ``(r, c)`` is a node connected to its in-bounds
4-directional neighbours. `grid_neighbors` is the helper every matrix problem needs.

Graphs here are ``dict[node, list[node]]`` adjacency lists.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Hashable, Iterable


def bfs(graph: dict, start: Hashable) -> list:
    """Breadth-first visit order from ``start`` (nodes in the order first reached)."""
    visited = {start}
    order = []
    queue: deque = deque([start])
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, ()):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order


def dfs(graph: dict, start: Hashable) -> list:
    """Depth-first visit order from ``start`` (recursive)."""
    visited: set = set()
    order: list = []

    def visit(node: Hashable) -> None:
        visited.add(node)
        order.append(node)
        for neighbor in graph.get(node, ()):
            if neighbor not in visited:
                visit(neighbor)

    visit(start)
    return order


def grid_neighbors(grid: list, row: int, col: int) -> Iterable[tuple[int, int]]:
    """Yield the in-bounds 4-directional neighbours of ``(row, col)`` in a 2D grid."""
    num_rows, num_cols = len(grid), len(grid[0])
    for d_row, d_col in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        r, c = row + d_row, col + d_col
        if 0 <= r < num_rows and 0 <= c < num_cols:
            yield (r, c)
