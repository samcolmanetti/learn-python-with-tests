from __future__ import annotations

import heapq


def min_cost_grid(grid: list[list[int]]) -> int:
    """Return the cheapest cost to walk from the top-left cell to the bottom-right.

    Each cell holds a non-negative entry cost. You may step up, down, left, or right,
    and you pay a cell's cost every time you enter it (the start cell included). Return
    ``-1`` if the grid is empty.
    """
    if not grid or not grid[0]:
        return -1

    rows, cols = len(grid), len(grid[0])
    start, goal = (0, 0), (rows - 1, cols - 1)

    dist: dict[tuple[int, int], int] = {start: grid[0][0]}
    heap: list[tuple[int, tuple[int, int]]] = [(grid[0][0], start)]
    while heap:
        d, (r, c) = heapq.heappop(heap)
        if (r, c) == goal:
            return d
        if d > dist[(r, c)]:
            continue
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                candidate = d + grid[nr][nc]
                if candidate < dist.get((nr, nc), float("inf")):
                    dist[(nr, nc)] = candidate
                    heapq.heappush(heap, (candidate, (nr, nc)))

    return dist[goal]
