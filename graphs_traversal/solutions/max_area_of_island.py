from __future__ import annotations

from .. import _template


def max_area_of_island(grid: list[list[int]]) -> int:
    if not grid or not grid[0]:
        return 0

    visited: set[tuple[int, int]] = set()

    def area(row: int, col: int) -> int:
        stack = [(row, col)]
        visited.add((row, col))
        count = 0
        while stack:
            r, c = stack.pop()
            count += 1
            for nr, nc in _template.grid_neighbors(grid, r, c):
                if grid[nr][nc] == 1 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    stack.append((nr, nc))
        return count

    best = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 1 and (r, c) not in visited:
                best = max(best, area(r, c))

    return best
