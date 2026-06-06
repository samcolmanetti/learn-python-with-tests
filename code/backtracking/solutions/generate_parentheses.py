from __future__ import annotations


def generate_parentheses(n: int) -> list[str]:
    result: list[str] = []
    path: list[str] = []

    def dfs(open_count: int, close_count: int) -> None:
        if len(path) == 2 * n:
            result.append("".join(path))
            return
        if open_count < n:
            path.append("(")  # choose
            dfs(open_count + 1, close_count)  # explore
            path.pop()  # un-choose
        if close_count < open_count:
            path.append(")")
            dfs(open_count, close_count + 1)
            path.pop()

    dfs(0, 0)
    return result
