# Linked Lists

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/linked_lists)**

A linked list is a chain of nodes, each holding a value and a pointer to the next one. There's no
random access, so almost every linked-list problem comes down to the same move: walk the chain and
rearrange `next` pointers carefully, often with two pointers running at different speeds.

## When to reach for linked-list moves

You're handed the `head` of a chain and asked to restructure it in place, or to find something a
fixed distance from an end you can't index into. Reach for these techniques when:

- You need to **reverse, merge, or splice** a list by rewiring `next` pointers instead of copying
  values into a new array.
- You need the **middle, the kth-from-end, or whether the list loops**, and you'd rather not make a
  first pass just to count the length. Two pointers at different speeds get you there in one pass.

The constraint that there's no random access is the whole pattern. If you find yourself wishing you
could write `nodes[i]`, you've stopped thinking like a linked list.

## The node

Everything in this chapter builds on one tiny class. Here it is from
[`linked_lists/_template.py`](linked_lists/_template.py):

```python
from __future__ import annotations

from collections.abc import Iterable


class ListNode:
    """A node in a singly linked list: a value and a pointer to the next node."""

    def __init__(self, val: int = 0, next: ListNode | None = None) -> None:
        self.val = val
        self.next = next

    def __repr__(self) -> str:
        return f"ListNode({self.val!r})"
```

A `ListNode` is just a value and a `next`. The last node's `next` is `None`, and that `None` is
how every walk knows when to stop. `head` is the first node (or `None` for an empty list), and
that single reference is all you ever get handed.

Typing out chains by hand (`ListNode(1, ListNode(2, ListNode(3)))`) gets old fast and reads badly
in a test. So the template ships two helpers: one to build a chain from a Python list, and one to
walk a chain back into a Python list so we can assert on it.

```python
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
```

`build_list` walks the values in reverse and prepends each one, so the head comes out first.
`to_list` is the canonical chain walk: start at `head`, append `node.val`, follow `node.next`,
stop at `None`. That `while node is not None` loop is the shape you'll write a hundred times. Burn
it in now.

These two are each other's inverse, so a round-trip should give back what you put in. That's worth
a test on its own, because everything downstream leans on these helpers being correct:

```python
from _template import ListNode, build_list, to_list


def test_build_then_to_list_round_trips():
    assert to_list(build_list([1, 2, 3])) == [1, 2, 3]


def test_build_empty_is_none():
    assert build_list([]) is None


def test_to_list_of_none_is_empty():
    assert to_list(None) == []
```

`uv run pytest` is green on these. Now we can write the real problems with chains that read like
ordinary lists.

## Problem 1: Reverse a linked list

> Given the head of a singly linked list, reverse it in place and return the new head.

This is the linked-list "hello world", and it's worth doing slowly, because the pointer dance here
shows up inside half the other problems.

### Write the test first

We build a chain, reverse it, and walk it back to a Python list to check. The helpers earn their
keep immediately: the test reads like it's about lists, not pointers.

```python
from _template import build_list, to_list
from reverse_list import reverse_list


def test_reverses_several_nodes():
    assert to_list(reverse_list(build_list([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]


def test_single_node_is_unchanged():
    assert to_list(reverse_list(build_list([1]))) == [1]


def test_empty_list_returns_none():
    assert reverse_list(build_list([])) is None


def test_two_nodes_swap():
    assert to_list(reverse_list(build_list([1, 2]))) == [2, 1]
```

The empty and single-node cases are the ones that catch a reversal written for the happy path
only. A loop that assumes there's always a `next` to grab will trip on both.

### Try to run the test

There's no `reverse_list` module yet, so the import is the first thing to break:

```
ImportError: cannot import name 'reverse_list' from 'linked_lists.solutions.reverse_list'
```

Listen to the error. It's pointing at the file we need to create.

### Write the minimal amount of code for the test to run and check the failing test output

Give it a `reverse_list` that returns `None`. It's wrong on purpose. We just want the test to run
so we can watch it fail on the value, which proves the test is checking what we think it is.

```python
from __future__ import annotations

from _template import ListNode


def reverse_list(head: ListNode | None) -> ListNode | None:
    return None
```

Run `uv run pytest`:

```
    def test_reverses_several_nodes():
>       assert to_list(reverse_list(build_list([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]
E       assert [] == [5, 4, 3, 2, 1]
E         Right contains 5 more items, first extra item: 5
```

It fails on the value, not on a missing name. `test_empty_list_returns_none` passes, but only
because our stub happens to return `None`, which is the right answer for that one case. The others
fail for the right reason. Time to do the real work.

### Write enough code to make it pass

Walk the list with three pointers in play: `prev` (the part already reversed), `current` (the node
we're looking at), and a stash of `current.next` so we don't lose the rest of the chain the instant
we rewire it. That stash is the whole trick. The moment you set `current.next = prev`, the original
`next` is gone, so you have to grab it first.

```python
from __future__ import annotations

from _template import ListNode


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
```

Green.

Read the loop body as four steps in order: remember where we were going (`nxt`), flip this node's
pointer backwards (`current.next = prev`), then slide both pointers forward (`prev = current`,
`current = nxt`). When `current` falls off the end and becomes `None`, `prev` is sitting on the old
last node, which is the new head. That's why we return `prev`, not `head`.

The empty list never enters the loop, so `prev` stays `None` and we return it. The single-node case
runs the loop once and returns that one node pointing at `None`. Both edge cases fall out of the
same code with no special branch.

### Refactor

There's nothing to tidy in eight lines, but it's worth naming the shape. This is the *three-pointer
reversal*, and you'll see the same `nxt = current.next; current.next = prev` pair embedded in
harder problems (reverse in groups of k, reverse the second half before comparing for a palindrome).
Learn it as one fluid motion. Re-run the tests to confirm nothing moved.

## Problem 2: Find the middle node

> Return the middle node of the list. If there are two middle nodes (an even-length list), return
> the second one.

The obvious approach is two passes: walk once to count `n`, walk again `n // 2` steps. That works,
but there's a one-pass trick that's worth having in your fingers.

### Write the test first

We assert by walking from the returned node to the end, so `to_list` shows us both *which* node we
landed on and what trails after it. That's a stronger check than just reading one value.

```python
from _template import build_list, to_list
from middle_node import middle_node


def test_odd_length_picks_exact_middle():
    assert to_list(middle_node(build_list([1, 2, 3, 4, 5]))) == [3, 4, 5]


def test_even_length_picks_second_middle():
    assert to_list(middle_node(build_list([1, 2, 3, 4, 5, 6]))) == [4, 5, 6]


def test_single_node_is_its_own_middle():
    assert to_list(middle_node(build_list([1]))) == [1]


def test_two_nodes_returns_second():
    assert to_list(middle_node(build_list([1, 2]))) == [2]
```

The even-length cases pin down the tie-break. For `[1, 2, 3, 4, 5, 6]` the two middles are `3` and
`4`, and the spec says return `4`. A solution that returns `3` is a different (also common) variant,
so we nail down which one we want.

### Try to run the test

No module yet:

```
ImportError: cannot import name 'middle_node' from 'linked_lists.solutions.middle_node'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return `head`. For most inputs that's the front of the list, not the middle, so we'll
see honest failures.

```python
from __future__ import annotations

from _template import ListNode


def middle_node(head: ListNode | None) -> ListNode | None:
    return head
```

Run `uv run pytest`:

```
    def test_odd_length_picks_exact_middle():
>       assert to_list(middle_node(build_list([1, 2, 3, 4, 5]))) == [3, 4, 5]
E       assert [1, 2, 3, 4, 5] == [3, 4, 5]
E         At index 0 diff: 1 != 3
```

It returns the whole list because we handed back the head. `test_single_node_is_its_own_middle`
passes, since for a one-node list the head genuinely is the middle. The rest fail on the value.
Good.

### Write enough code to make it pass

Run two pointers from the head. `slow` takes one step per iteration, `fast` takes two. By the time
`fast` reaches the end, `slow` has covered exactly half the distance, so it's parked on the middle.
This is the *fast and slow* technique, sometimes called the tortoise and the hare.

```python
from __future__ import annotations

from _template import ListNode


def middle_node(head: ListNode | None) -> ListNode | None:
    """Return the middle node. With an even count, return the second of the two middles."""
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow
```

Green.

The loop condition is the part to stare at. We keep going while `fast` has both a current node and
a next node, because the line below reads `fast.next.next` and we mustn't dereference `None`. When
the list has an even length, `fast` lands exactly on `None` after the last node and `slow` is on the
*second* middle, which is the tie-break the spec asked for. With an odd length, `fast` stops on the
final node (its `next` is `None`) and `slow` sits dead centre. The even and odd cases differ only in
where `fast` halts, and `slow` ends up right either way.

### Refactor

No tidy-up needed, but notice what we avoided: we never counted the list. **One pass, no length,
two pointers at different speeds.** That same fast/slow setup, with one extra check, solves the next
problem too, so keep it in mind. Re-run the tests.

## Problem 3: Merge two sorted lists

> Given the heads of two sorted linked lists, splice them into one sorted list and return its head.

We could pour both lists into an array, sort, and rebuild, but that throws away the work the inputs
already did for us: they're sorted. Better to weave them together by rewiring pointers, picking the
smaller head each time.

### Write the test first

```python
from _template import build_list, to_list
from merge_two_sorted import merge_two_sorted


def test_interleaves_two_lists():
    merged = merge_two_sorted(build_list([1, 2, 4]), build_list([1, 3, 4]))
    assert to_list(merged) == [1, 1, 2, 3, 4, 4]


def test_one_list_empty():
    assert to_list(merge_two_sorted(build_list([]), build_list([0]))) == [0]


def test_both_lists_empty():
    assert merge_two_sorted(build_list([]), build_list([])) is None


def test_one_list_runs_out_first():
    merged = merge_two_sorted(build_list([1, 2]), build_list([3, 4, 5]))
    assert to_list(merged) == [1, 2, 3, 4, 5]
```

`test_one_list_runs_out_first` is the case that matters most: one list empties while the other still
has nodes. Whatever's left has to get attached in one go, not dropped. The duplicate `1`s in the
first test also check that equal values don't get skipped or doubled.

### Try to run the test

No module yet:

```
ImportError: cannot import name 'merge_two_sorted' from 'linked_lists.solutions.merge_two_sorted'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return `None`:

```python
from __future__ import annotations

from _template import ListNode


def merge_two_sorted(
    list1: ListNode | None, list2: ListNode | None
) -> ListNode | None:
    return None
```

Run `uv run pytest`:

```
    def test_interleaves_two_lists():
        merged = merge_two_sorted(build_list([1, 2, 4]), build_list([1, 3, 4]))
>       assert to_list(merged) == [1, 1, 2, 3, 4, 4]
E       assert [] == [1, 1, 2, 3, 4, 4]
E         Right contains 6 more items, first extra item: 1
```

`test_both_lists_empty` passes (two empty lists really do merge to `None`), the rest fail on the
value. Now make them all pass for the right reason.

### Write enough code to make it pass

Use a *dummy head*: a throwaway node that sits in front of the result so we always have a `tail` to
append to, even for the very first node. Without it, the first append is a special case (is the
result still empty?), and special cases are where bugs live.

```python
from __future__ import annotations

from _template import ListNode


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
```

Green.

Each turn of the loop links the smaller head onto `tail`, advances that list past the node we took,
and moves `tail` forward. The loop stops the instant either list runs dry. Then the single line
after the loop does the heavy lifting for `test_one_list_runs_out_first`: at most one list still has
nodes, and since both inputs were sorted, that remaining tail is already in order and bigger than
everything placed so far, so we hang it off `tail.next` in one move. We return `dummy.next`, the
real first node, and the throwaway `dummy` is forgotten.

Using `<=` rather than `<` keeps the merge *stable* (equal values from `list1` come first) and,
more importantly, guarantees we always make progress so the loop terminates.

### Refactor

The body is already tight. The idea worth lifting out is the dummy head: **whenever you're building
a new list and the first node is awkward, prepend a dummy and return `dummy.next`.** It turns "is
this the first node?" into a non-question. You'll reach for it again in remove-nth-from-end and
in partition-list. Re-run the tests.

## Problem 4: Detect a cycle

> Return `True` if the linked list has a cycle in it, that is, some node's `next` eventually points
> back to an earlier node.

A cycle means the chain never reaches `None`, so a naive walk loops forever. We need a way to notice
we're going in circles without keeping a set of every node we've visited.

### Write the test first

There's no `build_list` for a cyclic list (our helper only makes chains that end in `None`), so the
test file needs a small builder that links the tail back into the chain. We write it once, at the
top of the test:

```python
from _template import build_list
from has_cycle import has_cycle


def link_into_cycle(values, pos):
    """Build a list from ``values``, then point the last node at index ``pos`` (-1 for none)."""
    head = build_list(values)
    if head is None:
        return None
    nodes = []
    node = head
    while node is not None:
        nodes.append(node)
        node = node.next
    if pos >= 0:
        nodes[-1].next = nodes[pos]
    return head


def test_no_cycle_is_false():
    assert has_cycle(link_into_cycle([1, 2, 3, 4], -1)) is False


def test_tail_back_to_middle_is_true():
    assert has_cycle(link_into_cycle([3, 2, 0, -4], 1)) is True


def test_two_node_self_loop_is_true():
    assert has_cycle(link_into_cycle([1, 2], 0)) is True


def test_single_node_no_cycle_is_false():
    assert has_cycle(link_into_cycle([1], -1)) is False


def test_empty_list_is_false():
    assert has_cycle(build_list([])) is False
```

`link_into_cycle([3, 2, 0, -4], 1)` makes the last node point back at index `1`, so the walk loops
forever past `2, 0, -4, 2, 0, -4, ...`. The `pos = -1` cases leave the list ending in `None`, our
non-cyclic controls. **Note we use `to_list` nowhere here**: you can't flatten a cyclic list to a
Python list, which is exactly why detecting the cycle is the job.

### Try to run the test

No module yet:

```
ImportError: cannot import name 'has_cycle' from 'linked_lists.solutions.has_cycle'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return `False`:

```python
from __future__ import annotations

from _template import ListNode


def has_cycle(head: ListNode | None) -> bool:
    return False
```

Run `uv run pytest`:

```
    def test_tail_back_to_middle_is_true():
>       assert has_cycle(link_into_cycle([3, 2, 0, -4], 1)) is True
E       assert False is True
E        +  where False = has_cycle(ListNode(3))
```

The three non-cyclic tests pass, since `False` is their right answer, and the two cyclic ones fail.
That split tells us the test discriminates between the cases, which is what we want before writing
the real thing.

### Write enough code to make it pass

Reuse the fast/slow idea from the middle-node problem. `slow` moves one step, `fast` moves two. If
the list ends, `fast` hits `None` and we return `False`. But if there's a cycle, the two pointers
are trapped on the same loop, and the faster one keeps gaining on the slower until it laps it and
they land on the same node. This is *Floyd's cycle detection*, the tortoise and the hare again.

```python
from __future__ import annotations

from _template import ListNode


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
```

Green.

The loop condition is the same `fast is not None and fast.next is not None` guard as before, and for
the same reason: we read `fast.next.next`, so both have to exist. If the walk ever reaches that
guard and fails it, the list terminated and there's no cycle. The one new line is `if slow is fast`,
checked *after* both pointers move so they don't trivially match at the start where both sit on
`head`. We compare with `is`, not `==`, because we care whether they're the *same node*, not whether
two nodes happen to share a value.

Why are they guaranteed to meet? On a loop, each step closes the gap between `fast` and `slow` by
exactly one node, so the gap can't jump over zero. It shrinks to nothing, and they collide. (That's
the one bit of cleverness in the chapter, so I'll let it sit there.)

### Refactor

Nothing to tidy. The thing to take away is that **fast/slow pointers solve a whole family of
problems**: the middle node, the kth-from-end, and cycle detection are all the same two pointers
with a different stopping rule. The full Floyd algorithm goes one step further and finds *where* the
cycle starts by resetting one pointer to the head; we only needed the yes/no here. Re-run the tests.

## Wrapping up

- **A linked list is a chain of `ListNode`s, and the whole game is rewiring `next` pointers**, because
  there's no random access. The canonical walk is `while node is not None: ...; node = node.next`.
- **Three-pointer reversal** (`nxt = current.next; current.next = prev; prev = current; current = nxt`)
  flips a list in one pass and hides inside many harder problems.
- **Fast and slow pointers** find the middle, the kth-from-end, and cycles in one pass with no length
  count. The `fast and fast.next` guard keeps you from dereferencing `None`.
- **A dummy head** removes the "is this the first node?" special case whenever you build a new list,
  as in the merge. Return `dummy.next`.
- **Floyd's cycle detection** uses fast/slow and the fact that on a loop the gap shrinks by one each
  step, so the pointers must collide. Compare with `is`, not `==`.
