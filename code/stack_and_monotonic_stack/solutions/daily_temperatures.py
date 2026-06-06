from __future__ import annotations

from collections.abc import Sequence


def daily_temperatures(temps: Sequence[int]) -> list[int]:
    """For each day, how many days until a strictly warmer one, else ``0``."""
    result = [0] * len(temps)
    stack: list[int] = []  # indices of days still waiting for a warmer day
    for i, temp in enumerate(temps):
        while stack and temps[stack[-1]] < temp:
            j = stack.pop()
            result[j] = i - j
        stack.append(i)
    return result
