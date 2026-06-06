from __future__ import annotations


def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    result: list[list[int]] = []
    path: list[int] = []

    def dfs(start: int, remaining: int) -> None:
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            choice = candidates[i]
            if choice > remaining:
                continue
            path.append(choice)  # choose
            dfs(i, remaining - choice)  # explore (i, not i + 1: reuse allowed)
            path.pop()  # un-choose

    dfs(0, target)
    return result
