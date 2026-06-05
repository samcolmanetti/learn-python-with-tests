from __future__ import annotations

from .. import _template


def flood_fill(
    image: list[list[int]], row: int, col: int, color: int
) -> list[list[int]]:
    start_color = image[row][col]
    if start_color == color:
        return image

    stack = [(row, col)]
    image[row][col] = color
    while stack:
        r, c = stack.pop()
        for nr, nc in _template.grid_neighbors(image, r, c):
            if image[nr][nc] == start_color:
                image[nr][nc] = color
                stack.append((nr, nc))

    return image
