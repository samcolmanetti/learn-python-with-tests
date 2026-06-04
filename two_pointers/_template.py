"""Two Pointers — opposite-direction and same-direction templates.

Two pointers turn many O(n^2) brute forces into O(n) single passes by maintaining an
*invariant* between two indices.

- **Opposite direction**: pointers start at the two ends and move toward each other. Use when
  the array is sorted or symmetric (two-sum-sorted, valid palindrome, container with most
  water).
- **Same direction** (a.k.a. fast/slow, read/write): both start at the left; the fast pointer
  scans while the slow pointer marks a boundary. Use for in-place filtering (remove
  duplicates, move zeros) and sliding boundaries.

These are directional skeletons — adapt the `process`/`condition` hooks per problem.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Callable, TypeVar

T = TypeVar("T")


def two_pointers_opposite(
    arr: Sequence[T],
    should_move_left: Callable[[T, T], bool],
) -> tuple[int, int]:
    """Walk two pointers inward until they meet.

    ``should_move_left(left_val, right_val)`` decides which end advances. Returns the final
    ``(left, right)`` indices — most problems read off an answer as they go; this skeleton
    just shows the movement.
    """
    left, right = 0, len(arr) - 1
    while left < right:
        if should_move_left(arr[left], arr[right]):
            left += 1
        else:
            right -= 1
    return left, right


def two_pointers_same(arr: list[T], keep: Callable[[T], bool]) -> int:
    """In-place stable filter: keep only elements satisfying ``keep``.

    The slow pointer is the write head; the fast pointer reads. Returns the new logical
    length; ``arr[:length]`` holds the kept elements in order. This is the engine behind
    "remove duplicates / move zeros" style problems.
    """
    slow = 0
    for fast in range(len(arr)):
        if keep(arr[fast]):
            arr[slow] = arr[fast]
            slow += 1
    return slow
