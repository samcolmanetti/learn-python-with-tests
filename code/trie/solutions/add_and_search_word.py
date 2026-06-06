from __future__ import annotations


class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_word = False


class WordDictionary:
    def __init__(self) -> None:
        self.root = TrieNode()

    def add_word(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_word = True

    def search(self, word: str) -> bool:
        return self._search(word, 0, self.root)

    def _search(self, word: str, i: int, node: TrieNode) -> bool:
        if i == len(word):
            return node.is_word
        ch = word[i]
        if ch == ".":
            return any(self._search(word, i + 1, child) for child in node.children.values())
        child = node.children.get(ch)
        if child is None:
            return False
        return self._search(word, i + 1, child)
