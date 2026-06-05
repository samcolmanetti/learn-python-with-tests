# Dijkstra

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/dijkstra)**

Dijkstra's algorithm is an **interview pattern**: a reusable [`dijkstra/_template.py`](dijkstra/_template.py)
plus worked problems in `dijkstra/solutions/`, each built test-first. It finds the cheapest path from
one node to every other node in a graph whose edges have non-negative weights, and the engine is a
single `heapq`.

## When to reach for Dijkstra

Plain breadth-first search finds the path with the fewest *edges*. That's the right answer only when
every edge costs the same. The moment edges carry different weights, "fewest hops" and "cheapest" stop
agreeing, and you need Dijkstra. Reach for it when:

- You want the **shortest path by total weight** from a single source, and **every weight is non-negative**.
- The problem hands you a **weighted graph or a grid with per-cell costs**, and asks for a minimum total
  cost to reach somewhere.

The non-negative part is load-bearing. Dijkstra's whole trick is that once it settles a node it never
revisits it, and that's only safe when no later edge can make a path cheaper. If you have negative
edges, you want Bellman-Ford instead, which is a different chapter.

## The template

We represent the graph as an adjacency dict: each node maps to a list of `(neighbor, weight)` pairs.
`dijkstra(graph, start)` returns a dict from each reachable node to the cost of the cheapest path from
`start`.

```python
from __future__ import annotations

import heapq
from collections.abc import Hashable, Mapping, Sequence


def dijkstra(
    graph: Mapping[Hashable, Sequence[tuple[Hashable, float]]],
    start: Hashable,
) -> dict[Hashable, float]:
    dist: dict[Hashable, float] = {start: 0}
    heap: list[tuple[float, Hashable]] = [(0, start)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue
        for neighbor, weight in graph.get(node, ()):
            candidate = d + weight
            if candidate < dist.get(neighbor, float("inf")):
                dist[neighbor] = candidate
                heapq.heappush(heap, (candidate, neighbor))
    return dist
```

The invariant is the one that makes the whole thing work: **the first time we pop a node off the heap,
its distance is final.** Because `heapq` always hands back the smallest `(distance, node)` tuple, and
because every edge is non-negative, nothing we discover later can beat a node we've already popped at
its recorded distance. So we settle it once and move on.

Two lines earn their place. `if d > dist[node]: continue` is the *stale-entry skip*. We never delete
old entries from the heap; when we find a cheaper route to a node we just push a fresh tuple. So the
heap can hold several entries for the same node, and this line throws away the out-of-date ones the
moment they surface. And `dist.get(neighbor, float("inf"))` treats any node we haven't reached yet as
infinitely far, so the first real path to it always wins.

That's the engine. Every problem below is the same loop wearing a different costume.

## Problem 1: Network Delay Time

> A signal starts at one node and travels along directed edges, each taking some time. Return how long
> until *every* node has the signal, or `-1` if some node never gets it.

This is Dijkstra with one twist at the end. The cheapest path to each node is when that node hears the
signal, and the network is fully lit when the *slowest* of those arrivals happens. So we run Dijkstra,
then take the max over all distances. If we couldn't reach everyone, it's `-1`.

### Write the test first

The signature LeetCode uses is `network_delay_time(times, n, source)`, where `times` is a list of
`[u, v, w]` directed edges and the `n` nodes are labelled `1` to `n`.

```python
from .network_delay_time import network_delay_time


def test_reaches_all_nodes():
    times = [[2, 1, 1], [2, 3, 1], [3, 4, 1]]
    assert network_delay_time(times, 4, 2) == 2


def test_single_node_no_travel():
    assert network_delay_time([], 1, 1) == 0


def test_unreachable_node_returns_minus_one():
    times = [[1, 2, 1]]
    assert network_delay_time(times, 3, 1) == -1


def test_prefers_cheaper_two_hop_path():
    # 1 -> 2 directly costs 5, but 1 -> 3 -> 2 costs 1 + 1 = 2.
    times = [[1, 2, 5], [1, 3, 1], [3, 2, 1]]
    assert network_delay_time(times, 3, 1) == 2


def test_last_node_sets_the_time():
    times = [[1, 2, 1], [1, 3, 4]]
    assert network_delay_time(times, 3, 1) == 4
```

`test_unreachable_node_returns_minus_one` pins the `-1` rule, and `test_prefers_cheaper_two_hop_path`
checks we actually relax edges instead of just believing the first direct edge we see.

### Try to run the test

The module is empty, so the import is the first thing to break:

```
solutions/test_network_delay_time.py:1: in <module>
    from .network_delay_time import network_delay_time
E   ImportError: cannot import name 'network_delay_time' from 'network_delay_time'
```

No function, nothing to call. The error tells us where to start.

### Write the minimal amount of code for the test to run and check the failing test output

Give it a function that returns a stub `0` so the tests run. We're not solving anything yet, we just
want to see them fail on the value rather than on a missing name.

```python
from __future__ import annotations


def network_delay_time(times: list[list[int]], n: int, source: int) -> int:
    return 0
```

Run `uv run pytest`:

```
    def test_reaches_all_nodes():
        times = [[2, 1, 1], [2, 3, 1], [3, 4, 1]]
>       assert network_delay_time(times, 4, 2) == 2
E       assert 0 == 2
E        +  where 0 = network_delay_time([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2)
```

It runs and fails on the value, which is what we want. Notice `test_single_node_no_travel` passes,
because a lone node with no travel really does take `0` time, and that happens to be what our stub
returns. One accidental green proves nothing on its own.

### Write enough code to make it pass

Build the adjacency dict from the edge list, run the template loop, then collapse the distances down
to a single answer. If we didn't reach all `n` nodes, return `-1`; otherwise the answer is the latest
arrival, `max(dist.values())`.

```python
from __future__ import annotations

import heapq


def network_delay_time(times: list[list[int]], n: int, source: int) -> int:
    graph: dict[int, list[tuple[int, int]]] = {}
    for u, v, w in times:
        graph.setdefault(u, []).append((v, w))

    dist: dict[int, int] = {source: 0}
    heap: list[tuple[int, int]] = [(0, source)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue
        for neighbor, weight in graph.get(node, ()):
            candidate = d + weight
            if candidate < dist.get(neighbor, float("inf")):
                dist[neighbor] = candidate
                heapq.heappush(heap, (candidate, neighbor))

    if len(dist) < n:
        return -1
    return max(dist.values())
```

The tests pass.

The middle of this function is the template, copied almost character for character. Only the edges into
and out of it are problem-specific: the `setdefault` loop that turns `[u, v, w]` rows into the adjacency
dict, and the two lines at the end that turn "distance to every node" into "time to light the whole
network".

### Refactor

There's not much to tidy, but the `len(dist) < n` check is worth a second look. `dist` only ever holds
nodes we actually reached, so its size *is* the count of reachable nodes. If that's fewer than `n`, some
node never heard the signal and the answer is `-1`. We get the unreachable check for free from the
shape of `dist`, no separate visited-set bookkeeping required. Re-run the tests to confirm nothing moved.

## Problem 2: Minimum Cost Path Through a Grid

> Each cell of a grid holds a non-negative entry cost. Starting at the top-left, you may step up, down,
> left, or right, and you pay a cell's cost every time you enter it (including the start). Return the
> cheapest cost to reach the bottom-right.

If you could only move right and down, this would be a clean dynamic-programming chapter: each cell's
best cost is its own value plus the cheaper of the cell above and the cell to its left. But "up" and
"left" are allowed, so a cheap path might double back, and that circular dependency breaks the DP. A
grid is just a graph where each cell is a node and the edges go to its four neighbours, so we reach for
Dijkstra.

### Write the test first

```python
from .min_cost_grid import min_cost_grid


def test_single_cell():
    assert min_cost_grid([[5]]) == 5


def test_empty_grid():
    assert min_cost_grid([]) == -1


def test_single_row():
    assert min_cost_grid([[1, 2, 3]]) == 6


def test_classic_min_path():
    assert min_cost_grid([[1, 3, 1], [1, 5, 1], [4, 2, 1]]) == 7


def test_detour_beats_straight_line():
    # A down-then-right DP is forced through a 100 cell. Dijkstra walks the cheap
    # left column and bottom row instead: 1+1+1 down, then 1+1 across = 5.
    grid = [
        [1, 100, 1],
        [1, 100, 1],
        [1, 1, 1],
    ]
    assert min_cost_grid(grid) == 5
```

`test_detour_beats_straight_line` is the one that earns its keep. A right-and-down-only solver has to
cross one of those `100` cells to get from the top-left region to the bottom row. Four-directional
Dijkstra walks straight down the cheap left column and then across the bottom, total `5`. If your code
gets `5` here, it's genuinely searching the grid and not quietly assuming you only move right and down.

### Try to run the test

Empty module again, so the import fails first:

```
solutions/test_min_cost_grid.py:1: in <module>
    from .min_cost_grid import min_cost_grid
E   ImportError: cannot import name 'min_cost_grid' from 'min_cost_grid'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return `0` so the tests run:

```python
from __future__ import annotations


def min_cost_grid(grid: list[list[int]]) -> int:
    return 0
```

Run `uv run pytest`:

```
    def test_single_cell():
>       assert min_cost_grid([[5]]) == 5
E       assert 0 == 5
E        +  where 0 = min_cost_grid([[5]])
```

Every test fails on the value, even `test_empty_grid` (which wants `-1`, not `0`). Good, nothing is
passing by accident this time. Now let's make them pass for the right reason.

### Write enough code to make it pass

The nodes are `(row, col)` coordinates. The start's distance isn't `0`, it's `grid[0][0]`, because we
pay to stand on the start cell. From each cell we look at its four neighbours, and the edge cost of
moving into a neighbour is that neighbour's grid value. Everything else is the template.

```python
from __future__ import annotations

import heapq


def min_cost_grid(grid: list[list[int]]) -> int:
    if not grid or not grid[0]:
        return -1

    rows, cols = len(grid), len(grid[0])
    start, goal = (0, 0), (rows - 1, cols - 1)

    dist: dict[tuple[int, int], int] = {start: grid[0][0]}
    heap: list[tuple[int, tuple[int, int]]] = [(grid[0][0], start)]
    while heap:
        d, (r, c) = heapq.heappop(heap)
        if (r, c) == goal:
            return d
        if d > dist[(r, c)]:
            continue
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                candidate = d + grid[nr][nc]
                if candidate < dist.get((nr, nc), float("inf")):
                    dist[(nr, nc)] = candidate
                    heapq.heappush(heap, (candidate, (nr, nc)))

    return dist[goal]
```

Green.

We don't build an adjacency dict here. The grid *is* the graph, so we generate a cell's neighbours on
the fly from the four `(dr, dc)` direction offsets, bounds-checking each one. That's the only real
change from Problem 1: same heap, same relax step, same stale-entry skip.

### Refactor

There's an early `return d` the moment we pop the goal, and it's worth defending because it looks like a
shortcut that might be wrong. It isn't. By the invariant, the first time we pop a node its distance is
final, so the first time we pop the goal we already have its cheapest cost and there's no reason to keep
draining the heap. We could delete that line and fall through to `return dist[goal]` at the end and get
the same answer, just slower. **Popping the goal early is the standard way to ask Dijkstra for one
destination instead of all of them.** Re-run the tests to confirm both forms agree.

## Wrapping up

- **Dijkstra finds single-source shortest paths by total weight** when every edge is non-negative, using
  a `heapq` to always expand the closest unsettled node next.
- **The invariant is "first pop is final"**: because the heap hands back the smallest distance and edges
  can't be negative, a node's distance is settled the moment it's popped.
- **We never delete stale heap entries.** We push a fresh tuple on each improvement and skip outdated
  ones with `if d > dist[node]: continue`.
- **Every problem is the same loop in a costume.** An edge list, a grid, whatever the input, the work is
  building the neighbours and reading the answer back out of `dist`.
- **A grid is a graph.** When movement is four-directional, "minimum path sum" stops being clean DP and
  becomes Dijkstra over `(row, col)` nodes.

Next: [Union Find](union-find.md), for the connectivity questions where you don't care about path cost,
only about which nodes can reach each other at all.
