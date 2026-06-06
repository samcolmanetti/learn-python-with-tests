"""Grid DP, fill a 2D table where each cell depends on its neighbours above and left.

Most 2D grid DP problems share one shape: walk the grid top-left to bottom-right, and set
``dp[r][c]`` from the cells you've already computed (``dp[r - 1][c]`` above and ``dp[r][c - 1]``
to the left, sometimes ``dp[r - 1][c - 1]`` on the diagonal). The first row and first column are
the base cases, since they have no neighbour above or to the left.

The reusable skeleton below is that walk, with ``combine`` deciding how a cell folds in its
neighbours. Pass the function that fits the problem and you've solved it. Each worked problem in
``solutions/`` adapts this same shape.
"""

from __future__ import annotations

from collections.abc import Callable


def grid_dp(
    rows: int,
    cols: int,
    base: Callable[[int, int], float],
    combine: Callable[[float, float, float, float], float],
) -> list[list[float]]:
    """Fill a ``rows`` x ``cols`` table top-left to bottom-right.

    ``base(r, c)`` returns the value for any cell on the first row or first column (the cells
    with no neighbour above or to the left). ``combine(up, left, diag, here)`` returns the value
    for an interior cell from its three already-computed neighbours and a per-cell ``here`` hook
    (always ``0.0`` here; problems that need the grid value override this by closing over it).
    """
    dp = [[0.0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if r == 0 or c == 0:
                dp[r][c] = base(r, c)
            else:
                dp[r][c] = combine(dp[r - 1][c], dp[r][c - 1], dp[r - 1][c - 1], 0.0)
    return dp
