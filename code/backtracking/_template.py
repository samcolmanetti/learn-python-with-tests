"""Backtracking, combinatorial search via choose / explore / un-choose.

Backtracking is DFS over a tree of partial solutions. At each step you iterate the available
choices, *make* a choice (push it onto the path), recurse, then *undo* it (pop) so the next
choice starts clean. Prune invalid branches early to cut the search space.

Two everyday shapes:

- **Collect** (basic): gather every complete path (subsets, permutations, combinations).
- **Aggregate**: count or optimise over the leaves without materialising every path
  (number of ways, best score).

These concrete generators show the skeleton; adapt the "choices" and "is leaf" logic per
problem.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


def subsets(items: Sequence[T]) -> list[list[T]]:
    """Every subset (the power set), built by choosing to include each index or not."""
    result: list[list[T]] = []
    path: list[T] = []

    def dfs(start: int) -> None:
        result.append(path[:])  # every node is a valid subset
        for i in range(start, len(items)):
            path.append(items[i])  # choose
            dfs(i + 1)  # explore
            path.pop()  # un-choose

    dfs(0)
    return result


def permutations(items: Sequence[T]) -> list[list[T]]:
    """Every ordering of ``items`` (assumes distinct elements)."""
    result: list[list[T]] = []
    path: list[T] = []
    used = [False] * len(items)

    def dfs() -> None:
        if len(path) == len(items):  # leaf: a complete permutation
            result.append(path[:])
            return
        for i in range(len(items)):
            if used[i]:
                continue
            used[i] = True  # choose
            path.append(items[i])
            dfs()  # explore
            path.pop()
            used[i] = False  # un-choose

    dfs()
    return result
