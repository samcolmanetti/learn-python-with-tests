"""Trie (prefix tree), store strings by shared prefix for fast prefix queries.

Each node holds a map from the next character to a child node, plus a flag marking the end of
a complete word. Insertion and lookup are O(len(word)) and independent of how many words are
stored, which is why tries power autocomplete, spell-check, and word-search problems.
"""

from __future__ import annotations


class TrieNode:
    def __init__(self) -> None:
        self.children: dict = {}
        self.is_word = False


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_word = True

    def search(self, word: str) -> bool:
        """Whether the exact ``word`` was inserted."""
        node = self._walk(word)
        return node is not None and node.is_word

    def starts_with(self, prefix: str) -> bool:
        """Whether any inserted word starts with ``prefix``."""
        return self._walk(prefix) is not None

    def _walk(self, s: str) -> TrieNode | None:
        node = self.root
        for ch in s:
            node = node.children.get(ch)
            if node is None:
                return None
        return node
