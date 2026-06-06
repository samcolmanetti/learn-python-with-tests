"""Small string functions built test-first in ../strings.md.

Three things worth carrying out of this file:

- A ``str`` is immutable. You never change one in place; you build a new one. That is why
  ``+=`` in a loop is a trap (it copies the whole string every time, O(n^2) total) and why
  ``"".join(parts)`` is the fix (one allocation, O(n)).
- ``split`` with no argument splits on *runs* of whitespace and drops empties, which is exactly
  what you want for tidying messy input.
- Comparing two strings as anagrams is just asking whether they're the same multiset of
  characters, and a ``Counter`` is a multiset.
"""

from __future__ import annotations

from collections import Counter


def reverse_words(sentence: str) -> str:
    """Reverse the order of the words in ``sentence``.

    ``"the quick brown fox"`` becomes ``"fox brown quick the"``. We split into words, reverse
    the list with a slice, and join back with single spaces.
    """
    words = sentence.split()
    return " ".join(words[::-1])


def is_anagram(first: str, second: str) -> bool:
    """Return ``True`` when ``first`` and ``second`` use the same letters the same number of times.

    Case-insensitive, and spaces don't count, so ``"Dormitory"`` and ``"Dirty room"`` are
    anagrams. A ``Counter`` of the cleaned letters is a multiset; two strings are anagrams
    exactly when their multisets are equal.
    """
    return _letters(first) == _letters(second)


def _letters(text: str) -> Counter:
    cleaned = [char.lower() for char in text if not char.isspace()]
    return Counter(cleaned)


def normalize_whitespace(text: str) -> str:
    """Collapse every run of whitespace to a single space and strip the ends.

    ``"  hello   world  "`` becomes ``"hello world"``. ``str.split()`` with no argument does the
    hard part: it splits on runs of whitespace and drops the empty pieces, so joining with single
    spaces is all that's left.
    """
    return " ".join(text.split())


def join_lines(parts: list[str]) -> str:
    """Join ``parts`` into one string with newlines between them, O(n) via ``str.join``.

    This is the function the chapter contrasts with the ``+=``-in-a-loop anti-pattern. ``join``
    walks the list once, sizes the result, and fills it in a single pass.
    """
    return "\n".join(parts)
