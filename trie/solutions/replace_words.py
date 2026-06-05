from __future__ import annotations


class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_word = False


def replace_words(roots: list[str], sentence: str) -> str:
    root = TrieNode()
    for word in roots:
        node = root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_word = True

    def shortest_root(word: str) -> str:
        node = root
        for i, ch in enumerate(word):
            node = node.children.get(ch)
            if node is None:
                return word
            if node.is_word:
                return word[: i + 1]
        return word

    return " ".join(shortest_root(word) for word in sentence.split())
