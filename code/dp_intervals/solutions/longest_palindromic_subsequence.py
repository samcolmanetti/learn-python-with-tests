from __future__ import annotations


def longest_palindromic_subsequence(s: str) -> int:
    n = len(s)
    if n == 0:
        return 0
    table = [[0] * n for _ in range(n)]
    for i in range(n):
        table[i][i] = 1
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                inner = table[i + 1][j - 1] if length > 2 else 0
                table[i][j] = inner + 2
            else:
                table[i][j] = max(table[i + 1][j], table[i][j - 1])
    return table[0][n - 1]
