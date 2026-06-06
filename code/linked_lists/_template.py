"""Linked lists: the singly linked node plus helpers to build and compare lists.

A singly linked list is a chain of nodes. Each node holds a value and a reference to the
next node; the last node points at ``None``. There's no random access: to reach the kth node
you walk k pointers from the head. That constraint is the whole pattern. Most linked-list
problems are solved by walking the chain while carefully rearranging ``next`` pointers, often
with two pointers moving at different speeds.

``ListNode`` is the node. ``build_list`` turns a Python list into a chain so tests read
cleanly, and ``to_list`` walks a chain back into a Python list so we can assert on it.
"""

from __future__ import annotations

from collections.abc import Iterable


class ListNode:
    """A node in a singly linked list: a value and a pointer to the next node."""

    def __init__(self, val: int = 0, next: ListNode | None = None) -> None:
        self.val = val
        self.next = next

    def __repr__(self) -> str:
        return f"ListNode({self.val!r})"


def build_list(values: Iterable[int]) -> ListNode | None:
    """Build a chain from ``values`` and return its head (``None`` for an empty input)."""
    head: ListNode | None = None
    for value in reversed(list(values)):
        head = ListNode(value, head)
    return head


def to_list(head: ListNode | None) -> list[int]:
    """Walk a chain from ``head`` and collect its values into a Python list."""
    out: list[int] = []
    node = head
    while node is not None:
        out.append(node.val)
        node = node.next
    return out
