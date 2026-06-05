# Topological Sort

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/topological_sort)**

Topological sort is an **interview pattern**: a reusable [`topological_sort/_template.py`](topological_sort/_template.py)
plus worked problems in `topological_sort/solutions/`, each built test-first. Give it a graph of
"this must come before that" and it hands you an order where every arrow points forward, or tells
you that no such order exists because something depends on itself in a loop.

## When to reach for topological sort

The shape to spot is a pile of dependencies and a question about order. Tasks with prerequisites,
build steps, course schedules, package installs. Reach for it when:

- You have a **directed graph** and you need to lay the nodes out in a line so every edge `u -> v`
  has `u` before `v`. That line is a *topological order*.
- You need to know whether the dependencies are even satisfiable, that is, whether there's a
  **cycle**. The same algorithm answers both: if you can't place every node, there's a cycle.

The one rule it depends on: the graph has to be a *DAG*, a directed acyclic graph. The moment two
nodes wait on each other, there's no valid order, and a good topological sort says so rather than
looping forever.

## The template

We model a graph as an adjacency list: a dict from each node to the list of nodes it points at.
An edge `u -> v` reads as "u comes before v". The template uses *Kahn's algorithm*, which is the
breadth-first flavour of topological sort.

```python
from __future__ import annotations

from collections import deque


def topo_sort(graph: dict) -> list | None:
    """A topological ordering of ``graph``, or ``None`` if it contains a cycle."""
    indegree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            # A neighbor that never appears as a key (a pure sink) still needs an entry.
            indegree[neighbor] = indegree.get(neighbor, 0) + 1

    queue = deque(node for node, deg in indegree.items() if deg == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, ()):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return order if len(order) == len(indegree) else None
```

The whole thing turns on one number per node: its *in-degree*, the count of edges pointing at it.
A node with in-degree `0` has no unmet prerequisites, so it's safe to place next. We start the
queue with every such node, and each time we place one, we "remove" it by decrementing its
neighbours' in-degrees. A neighbour that drops to `0` has just had its last prerequisite satisfied,
so it joins the queue.

The cycle check is the clever part, and it costs nothing extra. **If the graph has a cycle, the
nodes in that cycle never reach in-degree `0`** (each is waiting on the next), so they never get
placed. When the loop ends we compare `len(order)` against the node count. Came up short? Something
was stuck in a loop. That's why the return type is `list | None`: `None` means "no valid order".

Two small details that bite people. We seed `indegree` with `indegree.get(neighbor, 0) + 1` so a
node that only ever appears as a *neighbour* (a sink, never a dict key) still gets counted. And we
read neighbours with `graph.get(node, ())` for the same reason, so a sink with no outgoing edges
doesn't blow up with a `KeyError`.

Now let's adapt this skeleton to two classic interview problems.

## Problem 1: Course Schedule

> You have `num_courses` courses labelled `0` to `num_courses - 1` and a list of prerequisite
> pairs `[course, needs]` meaning you must take `needs` before `course`. Return whether you can
> finish every course.

This is the cycle question wearing a hat. You can finish all the courses exactly when the
prerequisite graph is a DAG. If course `A` needs `B` and `B` needs `A`, you're stuck forever.

### Write the test first

The courses are integers and the input is a flat list of pairs, so this version builds the graph
itself rather than taking an adjacency dict. We only care about a `True`/`False` answer.

```python
from .course_schedule import can_finish


def test_no_prerequisites():
    assert can_finish(2, []) is True


def test_simple_chain():
    assert can_finish(2, [[1, 0]]) is True


def test_direct_cycle():
    assert can_finish(2, [[1, 0], [0, 1]]) is False


def test_longer_cycle():
    assert can_finish(3, [[1, 0], [2, 1], [0, 2]]) is False


def test_diamond_is_fine():
    assert can_finish(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) is True


def test_self_loop_is_a_cycle():
    assert can_finish(1, [[0, 0]]) is False
```

`test_longer_cycle` (a three-node loop, not just a mutual pair) and `test_self_loop_is_a_cycle` (a
course that requires itself) are the cases that pin down real cycle detection. A solution that only
checks for the obvious two-node swap quietly passes the easy tests and fails these.

### Try to run the test

The module exists but the function doesn't yet, so the import is what breaks first:

```
ImportError: cannot import name 'can_finish' from 'topological_sort.solutions.course_schedule'
```

Listen to the error. It's pointing us at the one name we need to define.

### Write the minimal amount of code for the test to run and check the failing test output

Give it a `can_finish` that always returns `False`. This is deliberately wrong, but it lets the
tests run so we can watch them fail on the value rather than on a missing name.

```python
from __future__ import annotations


def can_finish(num_courses, prerequisites):
    return False
```

Run `uv run pytest`:

```
    def test_no_prerequisites():
>       assert can_finish(2, []) is True
E       assert False is True
E        +  where False = can_finish(2, [])
```

Good. The tests run and fail on the answer. The cycle tests pass right now, but only because our
stub returns `False` for everything, which is the right answer for the wrong reason. We need code
that says `True` when it should.

### Write enough code to make it pass

This is the template with the graph built from the pairs and the cycle check turned into the
answer. We count how many courses we manage to place; if that's all of them, there was no cycle.

```python
from __future__ import annotations

from collections import deque


def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    graph: dict[int, list[int]] = {course: [] for course in range(num_courses)}
    indegree = [0] * num_courses
    for course, needs in prerequisites:
        graph[needs].append(course)
        indegree[course] += 1

    queue = deque(course for course in range(num_courses) if indegree[course] == 0)
    taken = 0
    while queue:
        course = queue.popleft()
        taken += 1
        for nxt in graph[course]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    return taken == num_courses
```

The tests pass.

The direction matters: a pair `[course, needs]` is an edge `needs -> course`, because `needs`
comes first. So we append `course` to `graph[needs]` and bump `course`'s in-degree. Because the
courses are a dense range `0..num_courses - 1`, we use a plain `indegree` list indexed by course
number instead of the template's dict, which is a touch faster and avoids the sink-key fiddliness:
every course already has an entry.

The self-loop case (`[0, 0]`) falls out for free. Course `0` points at itself, so its in-degree
starts at `1`, it never reaches the queue, `taken` stays `0`, and we return `False`.

### Refactor

There's nothing to tidy in the algorithm, but it's worth naming what changed from the template. We
never built an `order` list because we don't need the order here, only the count, so we carry a
single `taken` integer. **The "did we place every node" check is the cycle test**, and here we
return it directly as the answer. One pass over nodes and edges, O(V + E) time. Re-run the tests to
confirm nothing moved.

## Problem 2: Course Schedule II

> Same setup as before, but now return an actual order in which to take all the courses. If no
> valid order exists, return an empty list `[]`.

Problem 1 asked "is it possible?". This one asks "show me how". It's the same Kahn's algorithm, but
now the `order` list we were ignoring becomes the return value. The cycle case, where we can't place
everyone, returns `[]` instead of a partial order.

### Write the test first

A topological order usually isn't unique (a diamond has several valid orders), so testing for one
exact list would be brittle. Instead we check the *property* that defines a valid order: every
prerequisite lands before the course that needs it. The simple chain has only one possible order,
so that one we can pin exactly.

```python
from .course_schedule_ii import find_order


def _is_valid_order(num_courses, prerequisites, order):
    if len(order) != num_courses or set(order) != set(range(num_courses)):
        return False
    position = {course: i for i, course in enumerate(order)}
    for course, needs in prerequisites:
        if position[needs] >= position[course]:
            return False
    return True


def test_no_prerequisites_lists_every_course():
    order = find_order(2, [])
    assert _is_valid_order(2, [], order)


def test_simple_chain():
    assert find_order(2, [[1, 0]]) == [0, 1]


def test_diamond_orders_prerequisites_first():
    prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]
    order = find_order(4, prerequisites)
    assert _is_valid_order(4, prerequisites, order)


def test_cycle_returns_empty():
    assert find_order(2, [[1, 0], [0, 1]]) == []


def test_single_course():
    assert find_order(1, []) == [0]
```

The `_is_valid_order` helper is the interesting bit. It records each course's position in the
returned order, then checks that for every pair, `needs` sits at a lower index than `course`. That
accepts any correct ordering, which is what we want, and rejects an order that's missing a course
or puts a prerequisite too late.

### Try to run the test

Same story as before. The function isn't defined, so the import fails:

```
ImportError: cannot import name 'find_order' from 'topological_sort.solutions.course_schedule_ii'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub `find_order` to return `[]` so the tests run:

```python
from __future__ import annotations


def find_order(num_courses, prerequisites):
    return []
```

Run `uv run pytest`:

```
    def test_simple_chain():
>       assert find_order(2, [[1, 0]]) == [0, 1]
E       assert [] == [0, 1]
E
E         Right contains 2 more items, first extra item: 0
```

The empty stub passes `test_cycle_returns_empty` by luck (a cycle should return `[]`, and `[]` is
all our stub knows how to say), and fails everything that expects a real order. That's the failure
we want: it proves the order-building tests actually exercise the order.

### Write enough code to make it pass

Take the `can_finish` code and, instead of counting placements, collect them into an `order` list.
At the end, return the order if we placed everyone, otherwise the empty list.

```python
from __future__ import annotations

from collections import deque


def find_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    graph: dict[int, list[int]] = {course: [] for course in range(num_courses)}
    indegree = [0] * num_courses
    for course, needs in prerequisites:
        graph[needs].append(course)
        indegree[course] += 1

    queue = deque(course for course in range(num_courses) if indegree[course] == 0)
    order: list[int] = []
    while queue:
        course = queue.popleft()
        order.append(course)
        for nxt in graph[course]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    return order if len(order) == num_courses else []
```

The tests pass.

That last line is the whole difference from the boolean version. **When there's a cycle, `order`
holds only the nodes we could place, which is fewer than `num_courses`, so we throw it away and
return `[]`.** Returning a partial order would be a bug: it's not a valid schedule, it's the nodes
that weren't stuck in the loop. The empty list is the honest answer.

### Refactor

The two course solutions are now almost the same function, and you'd be right to itch at the
duplication. In a real codebase I'd factor out the shared Kahn's pass and have one return a count,
the other a list. For a chapter where each problem stands alone, I'm leaving them spelled out so
you can read either without flipping back. The point worth keeping is that **once you have the
order, the boolean answer is just `len(order) == num_courses`**, so Course Schedule is really
Course Schedule II with the order thrown away. Re-run the tests one more time.

## Wrapping up

- **Topological sort lays a DAG out in a line where every edge points forward.** Kahn's algorithm
  does it by repeatedly placing any node with in-degree `0` and decrementing its neighbours.
- **The same pass detects cycles for free.** If you can't place every node, the leftovers are stuck
  in a loop, so there's no valid order. Return `None` or `[]` to say so.
- **In-degree is the invariant**: a node is ready exactly when its in-degree hits `0`, meaning all
  its prerequisites are already placed.
- **A common variant** swaps the `deque` for a heap when you want the *lexicographically smallest*
  valid order, picking the smallest ready node each step instead of any ready node.

Next: [Dijkstra](dijkstra.md), where the queue becomes a priority queue and the thing you track
along the way is distance instead of in-degree.
