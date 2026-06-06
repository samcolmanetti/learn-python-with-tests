from __future__ import annotations

from .._template import ListNode


def middle_node(head: ListNode | None) -> ListNode | None:
    """Return the middle node. With an even count, return the second of the two middles."""
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow
