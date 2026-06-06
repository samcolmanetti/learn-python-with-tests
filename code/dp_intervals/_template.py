"""Sequence / interval DP, fill a table over subproblems indexed by positions.

Most sequence DP fills a 2D table where ``table[i][j]`` answers a question about a prefix of
one sequence (length ``i``) against a prefix of another (length ``j``), or about a sub-interval
``s[i:j + 1]`` of a single sequence. You build the table bottom-up so every cell a recurrence
needs is already filled before you read it.

Two shapes recur:

* **Dual-sequence DP** walks two strings and fills an ``(m + 1) x (n + 1)`` grid. The leading
  row and column are the empty-prefix base cases. ``longest_common_subsequence`` and
  ``edit_distance`` are this shape.
* **Interval DP** answers a question about ``s[i:j + 1]`` from shorter intervals. You iterate by
  interval length so the shorter answers exist first. ``longest_palindromic_subsequence`` is
  this shape.

The function below is the dual-sequence skeleton: allocate the grid with its base row and
column, then fill each interior cell from its already-computed neighbours.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TypeVar

T = TypeVar("T")


def fill_grid(
    a: Sequence[T],
    b: Sequence[T],
    base: Callable[[int, int], int],
    step: Callable[[list[list[int]], int, int], int],
) -> list[list[int]]:
    """Fill an ``(len(a) + 1) x (len(b) + 1)`` table bottom-up.

    ``base(i, j)`` fills the leading row and column (the empty-prefix cases). ``step(table, i, j)``
    computes an interior cell from neighbours already filled. The grid is returned so the caller
    can read its answer (usually the bottom-right corner) or walk it back for a reconstruction.
    """
    m, n = len(a), len(b)
    table = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        table[i][0] = base(i, 0)
    for j in range(n + 1):
        table[0][j] = base(0, j)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            table[i][j] = step(table, i, j)
    return table
