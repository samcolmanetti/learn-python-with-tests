"""Doubly linked list skeleton for O(1) recency tracking.

An LRU cache needs two things in O(1): look a key up by value, and reorder that key to
"most recently used". A dict gives you the first. A doubly linked list gives you the second:
each node knows its neighbours, so unlinking a node and splicing it back in are constant-time
pointer swaps, no shifting required.

The trick that keeps the code honest is the pair of *sentinel* nodes, ``head`` and ``tail``.
They are never real entries. Every real node lives strictly between them, so ``unlink`` and
``push_front`` never have to check for ``None`` neighbours or an empty list. The most recently
used node sits just after ``head``; the least recently used sits just before ``tail``.
"""

from __future__ import annotations

from typing import Any


class Node:
    """One link in the list. Holds a key/value and pointers to its neighbours."""

    def __init__(self, key: Any = None, value: Any = None) -> None:
        self.key = key
        self.value = value
        self.prev: Node | None = None
        self.next: Node | None = None


class DoublyLinkedList:
    """A list bracketed by two sentinels, with O(1) front insert and unlink."""

    def __init__(self) -> None:
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def push_front(self, node: Node) -> None:
        """Splice ``node`` in just after ``head`` (the most-recently-used slot)."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def unlink(self, node: Node) -> None:
        """Remove ``node`` from the list by joining its two neighbours."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def pop_back(self) -> Node:
        """Unlink and return the node just before ``tail`` (the least-recently-used one)."""
        node = self.tail.prev
        self.unlink(node)
        return node
