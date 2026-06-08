# Design: LRU Cache

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/design_lru_cache)**

"Design an LRU cache" is the interview question where the data structure *is* the answer. You're
asked for a fixed-size cache where both `get` and `put` run in O(1), and where the oldest unused
entry gets thrown out when you run out of room. The whole game is picking the structures that make
every operation constant time.

## When to reach for this design

An LRU (least recently used) cache shows up whenever you've got a bounded amount of fast storage
and an unbounded stream of things you might want to keep. Reach for this design when:

- You need **bounded memory with automatic eviction**: keep the last `k` things, drop the rest.
- Both reads and writes must be **O(1)**, so a plain list you scan or sort is out.
- "Recently used" matters: every `get` and every `put` has to count as *touching* an entry and
  bump it to the front of the queue.

A dict alone gives you O(1) lookup but no notion of order. A list gives you order but O(n) removal
from the middle. Neither one is enough on its own, and that tension is the lesson.

## The template

The piece that does the heavy lifting is a doubly linked list, so `design_lru_cache/_template.py`
is a small, reusable one. Each node knows its neighbours, so unlinking a node and splicing it back
in are constant-time pointer swaps. No shifting, no scanning.

```python
class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def push_front(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def unlink(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
```

The two nodes created in `__init__`, `head` and `tail`, are *sentinels*. They never hold a real
entry. Every real node lives strictly between them. That's the part worth memorising, because it's
what makes the pointer code boring: since a real node always has a node on each side, `unlink` and
`push_front` never have to check for a `None` neighbour or special-case the empty list.

We'll put the most recently used node right after `head`, and the least recently used right before
`tail`. So "promote to most recent" is `unlink` then `push_front`, and "evict the oldest" is
unlink whatever sits at `tail.prev`. Both O(1).

## Problem 1: LRU Cache

> Build an `LRUCache(capacity)` with `get(key)` returning the value or `-1` on a miss, and
> `put(key, value)` inserting or updating. Both run in O(1). When the cache is full, a `put` of a
> new key evicts the least recently used entry. Every `get` and `put` counts as a use.

The signal here is the explicit O(1) on both operations plus the eviction rule. That combination is
what forces the dict-plus-linked-list pairing: the dict finds a node by key, the list orders nodes
by recency, and both point at the same nodes so they can't drift apart.

### Write the test first

Let me write the behaviours down before reaching for any structure. The interesting cases aren't
the happy path, they're the ones that pin down *recency*: a `get` has to refresh an entry, and so
does updating an existing key.

```python
from lru_cache import LRUCache


def test_get_miss_returns_minus_one():
    cache = LRUCache(2)
    assert cache.get(1) == -1


def test_put_then_get_returns_value():
    cache = LRUCache(2)
    cache.put(1, 100)
    assert cache.get(1) == 100


def test_update_existing_key_overwrites_value():
    cache = LRUCache(2)
    cache.put(1, 100)
    cache.put(1, 200)
    assert cache.get(1) == 200


def test_eviction_drops_least_recently_used():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(3, 3)  # capacity is 2, so the oldest key (1) is evicted
    assert cache.get(1) == -1
    assert cache.get(2) == 2
    assert cache.get(3) == 3


def test_get_refreshes_recency():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.get(1)  # now 1 is most recently used, 2 is least
    cache.put(3, 3)  # evicts 2, not 1
    assert cache.get(2) == -1
    assert cache.get(1) == 1
    assert cache.get(3) == 3


def test_update_refreshes_recency():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(1, 10)  # updating 1 also makes it most recently used
    cache.put(3, 3)  # evicts 2
    assert cache.get(2) == -1
    assert cache.get(1) == 10
    assert cache.get(3) == 3


def test_capacity_one_keeps_only_latest():
    cache = LRUCache(1)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == -1
    assert cache.get(2) == 2
```

`test_get_refreshes_recency` is the one that earns its keep. After reading key `1`, the next
eviction has to drop `2`, not `1`, because the read counted as a use. A cache that only tracks
insertion order (and forgets that reads matter) sails through every other test and fails this one.

### Try to run the test

We import `LRUCache` from a module that doesn't exist yet, so the import is the first thing to
break:

```
ModuleNotFoundError: No module named 'design_lru_cache.solutions.lru_cache'
```

No module, no class, nothing. The error is telling us where to start.

### Write the minimal amount of code for the test to run and check the failing test output

Give it an `LRUCache` whose `get` always returns `-1` and whose `put` does nothing. It's honestly
wrong, and that's the point: we want the tests to run so we can watch them fail on behaviour rather
than on a missing name.

```python
from __future__ import annotations


class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity

    def get(self, key: int) -> int:
        return -1

    def put(self, key: int, value: int) -> None:
        return None
```

Run `uv run pytest`:

```
    def test_put_then_get_returns_value():
        cache = LRUCache(2)
        cache.put(1, 100)
>       assert cache.get(1) == 100
E       assert -1 == 100
E        +  where -1 = get(1)
```

The tests run and fail on the value. Notice `test_get_miss_returns_minus_one` actually passes,
because a miss is the one case where returning `-1` is correct. One green test off a stub like this
proves nothing on its own. The rest fail for the right reason, so now we build the real thing.

### Write enough code to make it pass

Now we wire the dict to the doubly linked list. The dict maps a key to its node, so a lookup is
O(1). The list orders nodes by recency. I'm inlining the linked-list helpers as private methods on
the class rather than importing the template, so the solution reads top to bottom on its own, but
they're the same `unlink` and `push_front` from the template.

```python
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
```

The tests pass.

Walk the two paths that matter. On a `get` hit, we unlink the node and push it back to the front,
so a read counts as a use and `test_get_refreshes_recency` passes. On a `put` of an existing key,
we do the same promotion after overwriting the value, which is why `test_update_refreshes_recency`
works. And eviction reads `self.tail.prev`: that's always the least recently used node, because
everything more recent got pushed in front of it. We delete it from *both* the list and the dict,
or the dict would leak a key that no longer exists.

**Storing the `key` on the node is the detail that makes eviction O(1).** When we evict, we have
the node but we also need to remove its entry from the dict, and the dict is keyed by `key`. Without
`node.key` we'd be stuck scanning the dict to find which key pointed at this node, which is O(n) and
defeats the entire design.

### Refactor

There's real duplication: `get`, the update branch of `put`, and the insert branch all do "unlink
if present, then push to front". Let me pull the promotion out into one helper and route everything
through it.

```python
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

    def _touch(self, node: _Node) -> None:
        self._unlink(node)
        self._push_front(node)

    def get(self, key: int) -> int:
        node = self.store.get(key)
        if node is None:
            return -1
        self._touch(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        node = self.store.get(key)
        if node is not None:
            node.value = value
            self._touch(node)
            return
        if len(self.store) >= self.capacity:
            lru = self.tail.prev
            self._unlink(lru)
            del self.store[lru.key]
        node = _Node(key, value)
        self.store[key] = node
        self._push_front(node)
```

Re-run the tests and they're still green. The `_touch` helper names the operation that was hiding
in three places, and the class reads as four small intentions: look up, touch, evict, insert.

A fair question: **why not just use `collections.OrderedDict`?** It maintains insertion order and
gives you `move_to_end` and `popitem(last=False)`, which is exactly an LRU cache in about five
lines. In real code I'd reach for it without a second thought. But the interview is asking whether
you understand *why* it's O(1), and `OrderedDict` is itself a dict plus a doubly linked list under
the hood. Building the list by hand once is how you earn the right to use the shortcut later.

## Wrapping up

- **An LRU cache is a dict for O(1) lookup plus a doubly linked list for O(1) recency**, with both
  structures pointing at the same nodes so they stay in sync.
- **Sentinel `head` and `tail` nodes** mean `unlink` and `push_front` never special-case an empty
  list or a `None` neighbour. That's why the pointer code stays short.
- **Every `get` and every `put` is a "touch"**: unlink the node and push it to the front. Eviction
  is whatever sits at `tail.prev`.
- **Store the key on the node** so eviction can delete from the dict in O(1) instead of scanning.
- The standard-library shortcut is `collections.OrderedDict` with `move_to_end` and
  `popitem(last=False)`, which is this same structure with the bookkeeping done for you.
