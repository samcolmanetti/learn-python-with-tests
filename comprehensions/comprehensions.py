"""List, dict, and set comprehensions, plus a lazy generator.

A comprehension is a single expression that builds a list, dict, or set from an iterable.
It replaces the ``result = []``/``for``/``append`` boilerplate with one readable line. A
generator looks almost identical but produces values one at a time, on demand, so it never
holds the whole sequence in memory.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator


def squares(numbers: list[int]) -> list[int]:
    """Square every number (a **list comprehension**)."""
    return [n * n for n in numbers]


def evens(numbers: list[int]) -> list[int]:
    """Keep only the even numbers (a list comprehension with a **filter**)."""
    return [n for n in numbers if n % 2 == 0]


def char_index_map(text: str) -> dict[str, int]:
    """Map each character to the index of its **last** occurrence (a **dict comprehension**)."""
    return {char: index for index, char in enumerate(text)}


def unique_lengths(words: list[str]) -> set[int]:
    """Collect the distinct word lengths (a **set comprehension**)."""
    return {len(word) for word in words}


def running_total(numbers: Iterable[int]) -> Iterator[int]:
    """Yield the cumulative total after each number (a **generator**).

    This is lazy: each ``yield`` hands back one value and pauses, so the caller can stop early
    and we never build the full list of totals.
    """
    total = 0
    for number in numbers:
        total += number
        yield total
