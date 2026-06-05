from __future__ import annotations

from .._template import ListNode


def reverse_list(head: ListNode | None) -> ListNode | None:
    """Reverse a singly linked list in place and return the new head."""
    prev: ListNode | None = None
    current = head
    while current is not None:
        nxt = current.next
        current.next = prev
        prev = current
        current = nxt
    return prev
