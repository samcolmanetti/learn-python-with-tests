# Graph Traversal

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/graphs_traversal)**

Graph traversal is the same breadth-first and depth-first walk you already know from trees, with
one new rule: a graph can loop back on itself, so you keep a `visited` set and never enter a node
twice. That one set is the whole difference. With it, BFS and DFS carry straight over, and a 2D
grid turns out to be a graph in disguise.

## When to reach for graph traversal

You're walking a structure of connected things and you want to visit each one, find a path, or
count connected groups. Reach for it when:

- You have an **explicit graph**: nodes with edges, usually a `dict[node, list[node]]` adjacency
  list. Friend networks, course prerequisites, package dependencies.
- You have a **grid** and the problem is about connected cells: islands, regions, flood fill,
  reachable area. Each cell `(r, c)` is a node, and its edges are the in-bounds neighbours.
- You need **shortest path in an unweighted graph** (that's BFS, which reaches nodes in order of
  distance) or you just need to **touch every node** (BFS or DFS, pick whichever reads cleaner).

The signal for the grid problems, which is most of this chapter, is "connected cells". The moment
you read "count the islands" or "fill the region", you're doing a graph traversal on a matrix.

## The template

The pattern lives in [`graphs_traversal/_template.py`](graphs_traversal/_template.py). Three small
functions: a BFS, a DFS, and a grid-neighbour helper.

```python
from collections import deque


def bfs(graph, start):
    visited = {start}
    order = []
    queue = deque([start])
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, ()):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order
```

BFS uses a queue. We pop from the front, record the node, and push every unseen neighbour. The
*invariant* is the one worth memorising: a node goes into `visited` the moment we enqueue it, not
when we dequeue it. Mark on enqueue and a node can never be queued twice, so the cycle `a -> b ->
a` stops dead instead of spinning forever.

```python
def dfs(graph, start):
    visited = set()
    order = []

    def visit(node):
        visited.add(node)
        order.append(node)
        for neighbor in graph.get(node, ()):
            if neighbor not in visited:
                visit(neighbor)

    visit(start)
    return order
```

DFS is the same walk with the queue swapped for the call stack. We mark the node, record it, then
recurse into each unseen neighbour. Same `visited` guard, same protection against cycles. If you'd
rather not recurse, an explicit `stack = [start]` with `stack.pop()` does the identical job, and
that's the shape we'll use for the grid problems because it never blows the recursion limit on a
big board.

```python
def grid_neighbors(grid, row, col):
    num_rows, num_cols = len(grid), len(grid[0])
    for d_row, d_col in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        r, c = row + d_row, col + d_col
        if 0 <= r < num_rows and 0 <= c < num_cols:
            yield (r, c)
```

`grid_neighbors` is the adapter that makes a matrix behave like a graph. Given a cell, it yields
the four orthogonal neighbours (up, down, left, right) that actually fall inside the board. No
diagonals, and nothing off the edge. Every grid problem in this chapter leans on it, so the
bounds check lives here once instead of being copy-pasted into every solution.

There's a test for the template at [`graphs_traversal/test_template.py`](graphs_traversal/test_template.py).
The cycle cases (`{1: [2], 2: [3], 3: [1]}`) are the ones that earn their keep: without the
`visited` set those tests would hang, not fail.

## Problem 1: Number of Islands

> Given a grid of `"1"` (land) and `"0"` (water), count the islands. An island is land connected
> 4-directionally, and the grid is surrounded by water.

The phrase "land connected 4-directionally" is the tell. Each `"1"` is a node, neighbouring `"1"`s
are edges, and an island is one connected component. We count components by traversing.

### Write the test first

```python
from number_of_islands import num_islands


def test_single_island():
    grid = [
        list("11110"),
        list("11010"),
        list("11000"),
        list("00000"),
    ]
    assert num_islands(grid) == 1


def test_three_islands():
    grid = [
        list("11000"),
        list("11000"),
        list("00100"),
        list("00011"),
    ]
    assert num_islands(grid) == 3


def test_diagonal_does_not_connect():
    grid = [
        list("10"),
        list("01"),
    ]
    assert num_islands(grid) == 2


def test_all_water():
    grid = [list("000"), list("000")]
    assert num_islands(grid) == 0


def test_empty_grid():
    assert num_islands([]) == 0
```

`test_diagonal_does_not_connect` is the case that pins down the rule we actually want: two cells
touching at a corner are *separate* islands, because `grid_neighbors` only goes orthogonal. A
solution that allowed diagonals would return `1` here and we'd catch it.

### Try to run the test

The module doesn't define `num_islands` yet, so the test file can't even be imported:

```
ModuleNotFoundError: No module named 'graphs_traversal.solutions.number_of_islands'
```

Listen to the error: it's telling us the very first thing to create is a module with that name and
that function in it.

### Write the minimal amount of code for the test to run and check the failing test output

Give it a `num_islands` that returns a stub `0`. We're not solving anything yet, we just want the
test to run so we can watch it fail on the value. That proves the test checks what we think it
does.

```python
def num_islands(grid):
    return 0
```

Run `uv run pytest`:

```
    def test_single_island():
        grid = [
            list("11110"),
            list("11010"),
            list("11000"),
            list("00000"),
        ]
>       assert num_islands(grid) == 1
E       assert 0 == 1
E        +  where 0 = num_islands([['1', '1', '1', '1', '0'], ...])
```

The grids with islands fail on the value, exactly as they should. `test_all_water` and
`test_empty_grid` pass, but only because they happen to expect `0`, which is all our stub knows
how to return. One green test on a stub proves nothing.

### Write enough code to make it pass

Here's the plan. Walk every cell. When we hit a `"1"` we haven't visited, that's a new island, so
bump the counter and then *sink* the whole island by traversing every connected `"1"` and marking
it visited. Sinking it means the outer scan won't count any of its cells again.

The traversal is the template's DFS, written with an explicit stack and `grid_neighbors` instead
of an adjacency list.

```python
from __future__ import annotations

import _template


def num_islands(grid: list[list[str]]) -> int:
    if not grid or not grid[0]:
        return 0

    visited: set[tuple[int, int]] = set()
    islands = 0

    def sink(row: int, col: int) -> None:
        stack = [(row, col)]
        visited.add((row, col))
        while stack:
            r, c = stack.pop()
            for nr, nc in _template.grid_neighbors(grid, r, c):
                if grid[nr][nc] == "1" and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    stack.append((nr, nc))

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "1" and (r, c) not in visited:
                islands += 1
                sink(r, c)

    return islands
```

The tests pass.

Two details carry the weight. We add a cell to `visited` the moment we push it on the stack, the
same mark-on-enqueue invariant from the template, so no cell is ever queued twice. And the early
`if not grid or not grid[0]` guard keeps `len(grid[0])` from blowing up on an empty board, which
is what `test_empty_grid` is checking.

### Refactor

The structure is already the shape we want: an outer scan that finds new components and an inner
traversal that consumes each one. The one thing worth naming is that we never built an adjacency
list. `grid_neighbors` *is* the adjacency list, computed on demand, so the grid never gets copied
into a graph. That's the trade for matrix problems: the graph is implicit and you generate edges
as you walk. Re-run the tests to confirm nothing moved.

## Problem 2: Flood Fill

> Start at a pixel in an image, and repaint it and every same-coloured pixel connected to it
> 4-directionally with a new colour. Return the image.

This is the same connected-component walk as islands, except instead of counting we recolour as we
go. It's the "paint bucket" tool from every image editor.

### Write the test first

```python
from flood_fill import flood_fill


def test_fills_connected_region():
    image = [
        [1, 1, 1],
        [1, 1, 0],
        [1, 0, 1],
    ]
    assert flood_fill(image, 1, 1, 2) == [
        [2, 2, 2],
        [2, 2, 0],
        [2, 0, 1],
    ]


def test_no_change_when_color_matches():
    image = [
        [0, 0, 0],
        [0, 1, 1],
    ]
    assert flood_fill(image, 1, 1, 1) == [
        [0, 0, 0],
        [0, 1, 1],
    ]


def test_single_pixel():
    image = [[5]]
    assert flood_fill(image, 0, 0, 9) == [[9]]


def test_diagonal_not_filled():
    image = [
        [1, 0],
        [0, 1],
    ]
    assert flood_fill(image, 0, 0, 7) == [
        [7, 0],
        [0, 1],
    ]
```

`test_no_change_when_color_matches` is the trap. If the new colour equals the colour already under
the start pixel, the obvious code repaints a cell to its own colour, then visits its same-coloured
neighbours, repaints them to the colour they already are, and loops forever because nothing ever
changes to stop it. That test is there to make us handle it.

### Try to run the test

No module yet:

```
ModuleNotFoundError: No module named 'graphs_traversal.solutions.flood_fill'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub `flood_fill` to return the image untouched so the tests run:

```python
def flood_fill(image, row, col, color):
    return image
```

Run `uv run pytest`:

```
    def test_fills_connected_region():
        image = [
            [1, 1, 1],
            [1, 1, 0],
            [1, 0, 1],
        ]
>       assert flood_fill(image, 1, 1, 2) == [[2, 2, 2], [2, 2, 0], [2, 0, 1]]
E       assert [[1, 1, 1], [...0], [1, 0, 1]] == [[2, 2, 2], [...0], [2, 0, 1]]
E         At index 0 diff: [1, 1, 1] != [2, 2, 2]
```

It fails because the returned image is unchanged, which is what a do-nothing stub gives us. Notice
`test_no_change_when_color_matches` passes already, since "do nothing" happens to be right when the
colour matches. We still have to make it pass for the *right* reason, not by accident.

### Write enough code to make it pass

Read the start colour first. If it already equals the target, return immediately, because that's
the no-op case and also the one that would loop forever. Otherwise walk the region with the
template's stack-based DFS, repainting every cell that still holds the start colour.

```python
from __future__ import annotations

import _template


def flood_fill(
    image: list[list[int]], row: int, col: int, color: int
) -> list[list[int]]:
    start_color = image[row][col]
    if start_color == color:
        return image

    stack = [(row, col)]
    image[row][col] = color
    while stack:
        r, c = stack.pop()
        for nr, nc in _template.grid_neighbors(image, r, c):
            if image[nr][nc] == start_color:
                image[nr][nc] = color
                stack.append((nr, nc))

    return image
```

Green across the board.

We don't need a separate `visited` set here, and that's the neat part. Repainting a cell to the
new colour *is* marking it visited: once it's the new colour it no longer equals `start_color`, so
the `if image[nr][nc] == start_color` check skips it next time. The image is its own visited set.
That only works because we checked `start_color == color` up front. Without that guard, repainting
to the same colour wouldn't change anything and the walk would never terminate.

### Refactor

Nothing to tidy in the algorithm, but it's worth contrasting it with islands. There we needed an
explicit `visited` set because the cells stayed `"1"` the whole time; the only way to know we'd
seen one was to record it. Here the act of solving the problem (recolouring) doubles as the visited
mark, so the set disappears. **Whenever the traversal mutates the thing it walks, ask whether that
mutation can stand in for `visited`.** Re-run the tests.

## Problem 3: Max Area of Island

> In a grid of `1` (land) and `0` (water), return the area of the largest island, or `0` if there
> is none. Area is the count of connected land cells.

This is islands again, with one twist: instead of `+1` per island, each traversal returns *how
many* cells it touched, and we keep the maximum. The skeleton is identical, so this one moves fast.

### Write the test first

```python
from max_area_of_island import max_area_of_island


def test_largest_of_several_islands():
    grid = [
        [1, 1, 0, 0, 0],
        [1, 0, 0, 1, 1],
        [0, 0, 0, 1, 1],
        [0, 1, 0, 0, 0],
    ]
    assert max_area_of_island(grid) == 4


def test_single_island():
    grid = [
        [1, 1, 1],
        [0, 1, 0],
    ]
    assert max_area_of_island(grid) == 4


def test_all_water():
    grid = [
        [0, 0],
        [0, 0],
    ]
    assert max_area_of_island(grid) == 0


def test_diagonal_islands_counted_separately():
    grid = [
        [1, 0],
        [0, 1],
    ]
    assert max_area_of_island(grid) == 1


def test_empty_grid():
    assert max_area_of_island([]) == 0
```

`test_largest_of_several_islands` has a 2-cell island and a 4-cell island; we want `4`, the bigger
one, not the first one found or the sum. `test_diagonal_islands_counted_separately` repeats the
orthogonal-only rule, so a max-area solution can't quietly start counting diagonals either.

### Try to run the test

No module yet:

```
ModuleNotFoundError: No module named 'graphs_traversal.solutions.max_area_of_island'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return `0`:

```python
def max_area_of_island(grid):
    return 0
```

Run `uv run pytest`:

```
    def test_largest_of_several_islands():
        grid = [
            [1, 1, 0, 0, 0],
            [1, 0, 0, 1, 1],
            [0, 0, 0, 1, 1],
            [0, 1, 0, 0, 0],
        ]
>       assert max_area_of_island(grid) == 4
E       assert 0 == 4
E        +  where 0 = max_area_of_island([[1, 1, 0, 0, 0], ...])
```

The grids with land fail on the value. `test_all_water` and `test_empty_grid` pass on the stub by
expecting `0`, the same free pass we saw with islands.

### Write enough code to make it pass

Take the islands structure and change two things: the traversal returns a count, and the outer
loop tracks `best` with `max` instead of incrementing a counter.

```python
from __future__ import annotations

import _template


def max_area_of_island(grid: list[list[int]]) -> int:
    if not grid or not grid[0]:
        return 0

    visited: set[tuple[int, int]] = set()

    def area(row: int, col: int) -> int:
        stack = [(row, col)]
        visited.add((row, col))
        count = 0
        while stack:
            r, c = stack.pop()
            count += 1
            for nr, nc in _template.grid_neighbors(grid, r, c):
                if grid[nr][nc] == 1 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    stack.append((nr, nc))
        return count

    best = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 1 and (r, c) not in visited:
                best = max(best, area(r, c))

    return best
```

The tests pass.

The one detail to watch is *where* we count. We do `count += 1` when a cell comes off the stack,
not when it goes on, so each cell is tallied exactly once even though it was added to `visited`
earlier. Mark on push (to dedupe), count on pop (to total). Mixing those up double-counts.

### Refactor

There's barely anything to refactor, which is the point. Number-of-islands, flood-fill, and
max-area-of-island are the same traversal with a different accumulator: count components, repaint
cells, or take a maximum. **Once you can write the grid DFS, the problem is just deciding what to
do at each cell.** Re-run the tests to confirm the safety net's still holding.

## Wrapping up

- **Graph traversal is tree traversal plus a `visited` set.** That one set is what makes cycles
  safe; mark a node the moment you enqueue or push it, never after.
- **BFS uses a queue and reaches nodes in distance order; DFS uses the call stack or an explicit
  stack and dives deep.** Same walk, same guard, pick whichever reads cleaner.
- **A grid is an implicit graph.** `grid_neighbors` generates the edges on demand, so you never
  build an adjacency list; the matrix is the graph.
- **The grid problems are one skeleton with three accumulators**: count connected components
  (islands), recolour them (flood fill), or measure the biggest (max area). When the traversal
  mutates what it walks, the mutation can replace `visited` entirely.
