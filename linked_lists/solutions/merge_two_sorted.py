from __future__ import annotations

from .._template import ListNode


def merge_two_sorted(
    list1: ListNode | None, list2: ListNode | None
) -> ListNode | None:
    """Merge two sorted lists into one sorted list and return its head."""
    dummy = ListNode()
    tail = dummy
    while list1 is not None and list2 is not None:
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next
    tail.next = list1 if list1 is not None else list2
    return dummy.next
