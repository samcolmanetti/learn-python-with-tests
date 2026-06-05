from __future__ import annotations

from .._template import ListNode


def has_cycle(head: ListNode | None) -> bool:
    """Return ``True`` if the list contains a cycle, using Floyd's two pointers."""
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
