"""LRU cache with O(1) ``get`` and ``put`` from a dict plus a doubly linked list.

The dict maps a key to its :class:`Node`, so a lookup is O(1). The list orders nodes by
recency, so promoting a node to most-recently-used or evicting the least-recently-used one
is O(1) too. Both structures point at the same nodes, so they never drift out of sync.
"""

from __future__ import annotations


class _Node:
    def __init__(self, key: int = 0, value: int = 0) -> None:
        self.key = key
        self.value = value
        self.prev: _Node | None = None
        self.next: _Node | None = None


class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.store: dict[int, _Node] = {}
        # Sentinels: most recent sits after head, least recent sits before tail.
        self.head = _Node()
        self.tail = _Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _unlink(self, node: _Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _push_front(self, node: _Node) -> None:
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        node = self.store.get(key)
        if node is None:
            return -1
        self._unlink(node)
        self._push_front(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        node = self.store.get(key)
        if node is not None:
            node.value = value
            self._unlink(node)
            self._push_front(node)
            return
        if len(self.store) >= self.capacity:
            lru = self.tail.prev
            self._unlink(lru)
            del self.store[lru.key]
        node = _Node(key, value)
        self.store[key] = node
        self._push_front(node)
