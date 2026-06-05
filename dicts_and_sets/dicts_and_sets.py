"""Dicts and sets: O(1) lookup, ``Counter``, ``defaultdict``, and set algebra.

Four worked functions that each lean on a different part of the dict/set toolbox:

- ``word_count`` tallies words with ``collections.Counter``.
- ``first_non_repeating_char`` uses a ``Counter`` plus insertion order.
- ``common_elements`` is set intersection (``&``).
- ``group_anagrams`` buckets words with ``collections.defaultdict``.
"""

from __future__ import annotations

from collections import Counter, defaultdict


def word_count(text: str) -> dict[str, int]:
    """Count how many times each whitespace-separated word appears.

    ``Counter`` is a ``dict`` subclass built for exactly this: feed it an iterable and it
    tallies. We return a plain ``dict`` so callers don't have to care it was a ``Counter``.
    """
    return dict(Counter(text.split()))


def first_non_repeating_char(text: str) -> str | None:
    """Return the first character that appears exactly once, or ``None`` if there isn't one.

    One pass to count every character, a second pass in the original order to find the first
    with a count of ``1``. Dicts preserve insertion order (guaranteed since Python 3.7), so the
    second pass walks the string left to right.
    """
    counts = Counter(text)
    for char in text:
        if counts[char] == 1:
            return char
    return None


def common_elements(a: list[int], b: list[int]) -> set[int]:
    """Return the values present in both lists, as a set.

    Converting to sets and taking the intersection (``&``) is O(n + m) and drops duplicates for
    free. The list version (a nested loop) is O(n * m).
    """
    return set(a) & set(b)


def group_anagrams(words: list[str]) -> list[list[str]]:
    """Group words that are anagrams of each other.

    Two words are anagrams when their sorted letters match, so the sorted string is a natural
    bucket key. ``defaultdict(list)`` hands us an empty list the first time we touch a key, so
    we never write the ``if key not in groups`` dance.
    """
    groups: dict[str, list[str]] = defaultdict(list)
    for word in words:
        key = "".join(sorted(word))
        groups[key].append(word)
    return list(groups.values())
