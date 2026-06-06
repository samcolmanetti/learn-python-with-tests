# Union Find

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/union_find)**

Union find (also called Disjoint Set Union, or DSU) answers two questions about a pile of things
that get merged into groups: "are these two in the same group?" and "merge these two groups". It's
a reusable [`union_find/_template.py`](union_find/_template.py) plus worked problems in
`union_find/solutions/`, each built test-first.

## When to reach for union find

The signal is *connectivity over a set of elements that only ever join together, never split*.
You're given edges, or pairs, or equivalences, and you need to know who ends up grouped with whom.

- You're **counting connected components** in an undirected graph, and you'd rather not write a BFS
  or DFS over an adjacency list to do it.
- You need to **detect a cycle in an undirected graph**: an edge whose two endpoints are already in
  the same group closes a loop.
- You're **merging accounts, friends, or equivalences** and asking "are these two related?" many
  times as the merges stream in.

The trick is that each group is a tree, and the root of the tree is the group's name. Asking "same
group?" is asking "same root?". Merging two groups is pointing one root at the other. With two
small optimisations, both operations run in effectively constant time.

## The template

Here's the skeleton we'll adapt for both problems. It already lives in `union_find/_template.py`,
tested.

```python
from __future__ import annotations

from collections.abc import Hashable


class UnionFind:
    def __init__(self) -> None:
        self._parent: dict = {}
        self._rank: dict = {}
        self.count = 0  # number of disjoint sets

    def find(self, x: Hashable) -> Hashable:
        if x not in self._parent:
            self._parent[x] = x
            self._rank[x] = 0
            self.count += 1
        root = x
        while self._parent[root] != root:
            root = self._parent[root]
        while self._parent[x] != root:  # path compression
            self._parent[x], x = root, self._parent[x]
        return root

    def union(self, a: Hashable, b: Hashable) -> bool:
        root_a, root_b = self.find(a), self.find(b)
        if root_a == root_b:
            return False
        if self._rank[root_a] < self._rank[root_b]:
            root_a, root_b = root_b, root_a
        self._parent[root_b] = root_a
        if self._rank[root_a] == self._rank[root_b]:
            self._rank[root_a] += 1
        self.count -= 1
        return True

    def connected(self, a: Hashable, b: Hashable) -> bool:
        return self.find(a) == self.find(b)
```

Every element points at a parent. Follow the parents up and you reach a *root*, an element that
points at itself. The root is the group's identity. `find` climbs to the root; `union` joins two
groups by hanging one root under the other; `connected` is just "same root?".

Two details make this fast. The first is *path compression*: as `find` climbs to the root, that
second `while` loop re-points every node it passed straight at the root, so the next `find` is a
short hop instead of a long climb. The second is *union by rank*: `rank` is a rough height of each
tree, and `union` always hangs the shorter tree under the taller one so the forest stays flat.
Together they give you near-constant-time operations.

One return value is worth pausing on. **`union` returns `True` when it actually merged two separate
groups, and `False` when the two were already together.** That boolean is the whole game for cycle
detection, and we'll lean on it hard in Problem 2.

We don't pre-size anything. `find` lazily adds an element the first time it sees one, bumping
`count` (the number of disjoint sets) as it goes. That keeps the structure usable with strings,
tuples, any `Hashable`, not just integers in a known range.

## Problem 1: Number of Connected Components

> You have `n` nodes labelled `0` to `n - 1` and a list of undirected `edges`. Return how many
> connected components the graph has.

This is the textbook use. Each edge says "these two belong together". After processing them all,
the number of groups left is the answer, and the template already keeps that running total in
`count`.

### Write the test first

```python
from number_of_connected_components import count_components


def test_two_components():
    assert count_components(5, [[0, 1], [1, 2], [3, 4]]) == 2


def test_one_component():
    assert count_components(5, [[0, 1], [1, 2], [2, 3], [3, 4]]) == 1


def test_no_edges():
    assert count_components(4, []) == 4


def test_redundant_edges_dont_double_count():
    assert count_components(3, [[0, 1], [1, 2], [0, 2]]) == 1


def test_single_node():
    assert count_components(1, []) == 1
```

`test_no_edges` pins down the base case: with no edges, every node is its own component.
`test_redundant_edges_dont_double_count` is the one that earns its keep. The edge `[0, 2]` joins
two nodes that are already connected through `1`, and a naive "subtract one per edge" count would
wrongly land on `0`. Union find handles it because that third `union` is a no-op on the count.

### Try to run the test

The module doesn't exist yet, so the import is the first thing to break:

```
ModuleNotFoundError: No module named 'union_find.solutions.number_of_connected_components'
```

No module, no function. The error is telling us exactly what to create.

### Write the minimal amount of code for the test to run and check the failing test output

Give it a `count_components` that returns a stub `0`. We're not solving anything yet. We just want
the test to run and fail on the value, which proves the test checks what we think it does.

```python
from __future__ import annotations


def count_components(n: int, edges: list[list[int]]) -> int:
    return 0
```

Run `uv run pytest`:

```
    def test_redundant_edges_dont_double_count():
>       assert count_components(3, [[0, 1], [1, 2], [0, 2]]) == 1
E       assert 0 == 1
E        +  where 0 = count_components(3, [[0, 1], [1, 2], [0, 2]])

FAILED ...::test_two_components
FAILED ...::test_one_component
FAILED ...::test_no_edges
FAILED ...::test_redundant_edges_dont_double_count
FAILED ...::test_single_node
```

All five fail on the value, not on a missing name. That's exactly the state we want before writing
the real thing.

### Write enough code to make it pass

Build a `UnionFind`, register every node so isolated ones still count, then union each edge. The
answer is `count`.

```python
from __future__ import annotations

from _template import UnionFind


def count_components(n: int, edges: list[list[int]]) -> int:
    uf = UnionFind()
    for node in range(n):
        uf.find(node)
    for a, b in edges:
        uf.union(a, b)
    return uf.count
```

The tests pass.

The first loop matters more than it looks. `find(node)` is what *registers* a node, and registering
bumps `count`. Without that loop, a node that appears in no edge would never get added, and
`test_no_edges` (four lonely nodes, expecting `4`) would come back as `0`. We seed all `n` nodes up
front, then let the unions pull `count` back down as groups merge.

You never told union find how many components there are. It counted as a side effect of merging:
each real `union` does `count -= 1`, and the redundant edge in `test_redundant_edges_dont_double_count`
returns early without touching it. That's why the double-counting case just works.

### Refactor

There's nothing to tidy in eight lines, but it's worth naming the shape. We didn't write any graph
traversal. No adjacency list, no visited set, no recursion. The components fell out of the merges.
Compared with a DFS that builds an adjacency list and walks it, this is less code and less state,
and it's the version I'd reach for under interview pressure. Re-run the tests to confirm nothing
moved.

## Problem 2: Redundant Connection

> You start with a tree of `n` nodes (labelled `1` to `n`) and someone adds one extra edge, making
> exactly one cycle. Given the edges in order, return the edge that closes the cycle. If several
> edges could be removed, return the one that appears last in the input.

A tree with `n` nodes has exactly `n - 1` edges and no cycles. Add one more edge and you create
exactly one cycle. We want the edge that closed it.

Here's the reframing that makes this a union-find problem. Walk the edges in order and union each
one. The moment `union` reports that the two endpoints were **already connected**, that edge didn't
join two separate groups, it linked two nodes that already had a path between them. That edge is the
one that closes the loop.

### Write the test first

```python
from redundant_connection import find_redundant_connection


def test_triangle():
    assert find_redundant_connection([[1, 2], [1, 3], [2, 3]]) == [2, 3]


def test_returns_last_edge_that_closes_the_loop():
    assert find_redundant_connection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]) == [1, 4]


def test_self_contained_cycle():
    assert find_redundant_connection([[1, 2], [2, 3], [3, 1]]) == [3, 1]


def test_first_redundant_edge_wins():
    assert find_redundant_connection([[1, 2], [1, 3], [2, 3], [3, 4]]) == [2, 3]
```

`test_returns_last_edge_that_closes_the_loop` is the careful one. Nodes `1`, `2`, `3`, `4` get
strung into a chain, then `[1, 4]` ties the chain into a loop, and `[1, 5]` dangles a fresh node off
the side. The cycle-closing edge is `[1, 4]`, and the trailing `[1, 5]` is there to check we don't
just grab the last edge in the list. Because we scan in order and return the *first* edge that finds
its endpoints already connected, we naturally land on the right one.

### Try to run the test

Same opening as before. Nothing to import yet:

```
ModuleNotFoundError: No module named 'union_find.solutions.redundant_connection'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return an empty list so the tests run:

```python
from __future__ import annotations


def find_redundant_connection(edges: list[list[int]]) -> list[int]:
    return []
```

Run `uv run pytest`:

```
    def test_triangle():
>       assert find_redundant_connection([[1, 2], [1, 3], [2, 3]]) == [2, 3]
E       assert [] == [2, 3]
E         
E         Right contains 2 more items, first extra item: 2
E         Use -v to get more diff
```

All four fail on the value. The stub runs, the import resolves, and now we can make them pass for
the right reason.

### Write enough code to make it pass

Union each edge in order. The first one whose `union` returns `False` (the endpoints were already in
the same group) is the answer.

```python
from __future__ import annotations

from _template import UnionFind


def find_redundant_connection(edges: list[list[int]]) -> list[int]:
    uf = UnionFind()
    for a, b in edges:
        if not uf.union(a, b):
            return [a, b]
    return []
```

Green.

This is the payoff for that boolean we flagged back in the template. `union(a, b)` does the find,
the rank comparison, and the merge, and hands back `True` or `False` to say whether a real merge
happened. We don't have to track which nodes we've seen or build any path-finding ourselves: if
`union` says "already connected", we've found our cycle edge and we return it. **The first edge that
fails to merge is the edge that closes the cycle**, and because we walk the input in order, "first
to fail" is exactly the last-in-input edge the problem asked for.

The trailing `return []` never fires on valid input (the problem guarantees a cycle exists), but it
keeps the function total and the type checker happy.

### Refactor

Four lines, nothing to compress. What's worth noticing is how little this problem looks like Problem
1 on the surface, "find the cycle edge" versus "count the groups", and how it's the same machine
underneath. One reads `count`, the other reads the return value of `union`. Same `UnionFind`, two
different questions. Re-run the tests.

## Wrapping up

- **Union find tracks connectivity over elements that only ever merge.** Each group is a tree, the
  root names the group, and "same group?" is "same root?".
- **Path compression and union by rank** keep the trees flat, so `find`, `union`, and `connected`
  all run in effectively constant time.
- **Counting components is a side effect of merging**: register every node, union the edges, read
  `count`. No traversal, no visited set.
- **`union` returning `False` means the two were already connected.** That single boolean is cycle
  detection in an undirected graph: the first edge that fails to merge is the one that closes the
  loop.

Next: [Topological Sort](topological-sort.md), where we order a directed graph instead of grouping
an undirected one, and the cycle we want to detect breaks the ordering rather than closing a loop.
