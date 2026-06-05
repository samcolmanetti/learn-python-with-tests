from __future__ import annotations

DIGIT_LETTERS = {
    "2": "abc",
    "3": "def",
    "4": "ghi",
    "5": "jkl",
    "6": "mno",
    "7": "pqrs",
    "8": "tuv",
    "9": "wxyz",
}


def letter_combinations(digits: str) -> list[str]:
    if not digits:
        return []

    result: list[str] = []
    path: list[str] = []

    def dfs(index: int) -> None:
        if index == len(digits):
            result.append("".join(path))
            return
        for letter in DIGIT_LETTERS[digits[index]]:
            path.append(letter)  # choose
            dfs(index + 1)  # explore
            path.pop()  # un-choose

    dfs(0)
    return result
