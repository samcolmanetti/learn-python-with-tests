from __future__ import annotations


class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_word = False


def longest_word(words: list[str]) -> str:
    root = TrieNode()
    for word in words:
        node = root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_word = True

    best = ""

    def visit(node: TrieNode, built: str) -> None:
        nonlocal best
        if len(built) > len(best) or (len(built) == len(best) and built < best):
            best = built
        for ch in sorted(node.children):
            child = node.children[ch]
            if child.is_word:
                visit(child, built + ch)

    visit(root, "")
    return best
