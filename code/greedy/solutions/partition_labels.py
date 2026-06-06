from __future__ import annotations


def partition_labels(s: str) -> list[int]:
    last = {char: i for i, char in enumerate(s)}

    sizes = []
    start = 0
    end = 0
    for i, char in enumerate(s):
        end = max(end, last[char])
        if i == end:
            sizes.append(end - start + 1)
            start = i + 1
    return sizes
