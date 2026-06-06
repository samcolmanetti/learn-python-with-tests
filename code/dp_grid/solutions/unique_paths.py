from __future__ import annotations


def unique_paths(rows: int, cols: int) -> int:
    if rows == 0 or cols == 0:
        return 0
    dp = [[1] * cols for _ in range(rows)]
    for r in range(1, rows):
        for c in range(1, cols):
            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]
    return dp[rows - 1][cols - 1]
