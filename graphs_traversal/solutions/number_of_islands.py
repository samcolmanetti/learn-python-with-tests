from __future__ import annotations

from .. import _template


def num_islands(grid: list[list[str]]) -> int:
    if not grid or not grid[0]:
        return 0

    visited: set[tuple[int, int]] = set()
    islands = 0

    def sink(row: int, col: int) -> None:
        stack = [(row, col)]
        visited.add((row, col))
        while stack:
            r, c = stack.pop()
            for nr, nc in _template.grid_neighbors(grid, r, c):
                if grid[nr][nc] == "1" and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    stack.append((nr, nc))

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "1" and (r, c) not in visited:
                islands += 1
                sink(r, c)

    return islands
