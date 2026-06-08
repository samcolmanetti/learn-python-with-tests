# DP on a Grid

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/dp_grid)**

Grid DP is the same dynamic-programming idea you met in one dimension, laid out on a 2D table:
each cell's answer is built from the cells you've already filled in above it and to its left. We'll
keep a reusable shape in [`dp_grid/_template.py`](dp_grid/_template.py) and work three problems in
`dp_grid/solutions/`, each test-first.

## When to reach for grid DP

You're handed a 2D grid (or two strings, which form an implicit grid), and the answer for one cell
depends only on its neighbours. Reach for grid DP when:

- You're moving through a grid **one step at a time**, usually right or down, and you want to count
  the paths or find the best one. The number of ways to reach a cell is the sum of the ways to
  reach the cells you could have stepped from.
- You're measuring a **local 2D shape**, like the largest all-ones square, where a cell's answer
  is one more than the worst of the three cells touching its top-left corner.

The common thread: fill a `dp` table top-left to bottom-right, and every interior cell reads only
`dp[r - 1][c]` (above), `dp[r][c - 1]` (left), and sometimes `dp[r - 1][c - 1]` (the diagonal).
The first row and first column are the base cases, because they have no neighbour above or to the
left.

## The template

```python
from __future__ import annotations

from collections.abc import Callable


def grid_dp(
    rows: int,
    cols: int,
    base: Callable[[int, int], float],
    combine: Callable[[float, float, float, float], float],
) -> list[list[float]]:
    dp = [[0.0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if r == 0 or c == 0:
                dp[r][c] = base(r, c)
            else:
                dp[r][c] = combine(dp[r - 1][c], dp[r][c - 1], dp[r - 1][c - 1], 0.0)
    return dp
```

The skeleton is just the walk: allocate a `rows` by `cols` table, sweep it top-left to
bottom-right, and ask `combine` how an interior cell folds in its three already-computed
neighbours. The *invariant* is the part worth holding onto: **by the time we compute `dp[r][c]`,
every cell it depends on is already final**, because we filled rows top to bottom and each row left
to right.

Notice the order of the loops gives us that for free. `dp[r - 1][c]` was written on the previous
row, and `dp[r][c - 1]` was written one column ago on this row. No cell is ever read before it's
done.

In real problems you rarely import `grid_dp` and pass two lambdas; the per-problem code is clearer
inlined. The template is here to fix the *shape* in your head so each problem below is a small
variation on one walk, not three new algorithms.

## Problem 1: Unique Paths

> A robot sits in the top-left corner of a `rows` by `cols` grid. It can only move right or down.
> How many distinct paths reach the bottom-right corner?

The signal is "only right or down" plus "how many paths". To stand on a cell you must have arrived
from the cell above it or the cell to its left, so the count of paths to a cell is the sum of the
counts to those two.

### Write the test first

```python
from unique_paths import unique_paths


def test_three_by_seven():
    assert unique_paths(3, 7) == 28


def test_three_by_two():
    assert unique_paths(3, 2) == 3


def test_single_row():
    assert unique_paths(1, 5) == 1


def test_single_cell():
    assert unique_paths(1, 1) == 1


def test_square():
    assert unique_paths(4, 4) == 20


def test_empty_grid():
    assert unique_paths(0, 5) == 0
```

`test_single_row` and `test_single_cell` pin the base cases: with only one row (or one cell) there's
exactly one path, since you never get to choose. `test_empty_grid` is the degenerate case where
there's no destination at all.

### Try to run the test

The module doesn't exist yet, so the import is the first thing to break:

```
ModuleNotFoundError: No module named 'dp_grid.solutions.unique_paths'
```

Listen to the error. It's telling us exactly which file to create.

### Write the minimal amount of code for the test to run and check the failing test output

Give it a `unique_paths` that returns a stub `0`. We're not solving anything yet. We just want the
test to run so we can watch it fail on the value, which proves the test checks what we think.

```python
from __future__ import annotations


def unique_paths(rows: int, cols: int) -> int:
    return 0
```

Run `uv run pytest`:

```
    def test_three_by_seven():
>       assert unique_paths(3, 7) == 28
E       assert 0 == 28
E        +  where 0 = unique_paths(3, 7)
```

The test runs and fails on the value, not on a missing name. The one test that passes is
`test_empty_grid`, and it only passes because it happens to expect `0`, which is what our stub
returns. **One green test on a stub proves nothing.**

### Write enough code to make it pass

Fill a table of ones (the first row and first column each have a single path), then every interior
cell is the sum of the cell above and the cell to the left.

```python
from __future__ import annotations


def unique_paths(rows: int, cols: int) -> int:
    if rows == 0 or cols == 0:
        return 0
    dp = [[1] * cols for _ in range(rows)]
    for r in range(1, rows):
        for c in range(1, cols):
            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]
    return dp[rows - 1][cols - 1]
```

Run the tests again and they're green.

Seeding the whole grid with `1` does double duty: it sets the base cases (the top row and left
column stay `1`) and gives interior cells a harmless starting value we immediately overwrite. The
guard `if rows == 0 or cols == 0` handles the empty grid before we try to index `dp[rows - 1]`,
which would otherwise blow up.

### Refactor

This is exactly the template's walk with `base(r, c) = 1` and `combine = up + left`, so there's no
algorithm to tidy. The diagonal goes unused here, which is normal: path-counting only ever steps
from above or the left. I'd leave the inlined version as is, because spelling the recurrence out in
the loop reads better than threading two lambdas through `grid_dp`. Re-run the tests to confirm
nothing moved.

## Problem 2: Minimum Path Sum

> Given a grid of non-negative numbers, find a path from the top-left to the bottom-right that
> minimises the sum of the numbers along it. You may only move right or down.

Same movement rules as before, but now each cell carries a cost and we want the cheapest path, not
the count of paths. The recurrence barely changes: the cheapest way to *reach* a cell is its own
cost plus the cheaper of the two ways in.

### Write the test first

```python
from min_path_sum import min_path_sum


def test_classic():
    grid = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
    assert min_path_sum(grid) == 7


def test_single_row():
    assert min_path_sum([[1, 2, 3]]) == 6


def test_single_column():
    assert min_path_sum([[1], [2], [3]]) == 6


def test_single_cell():
    assert min_path_sum([[5]]) == 5


def test_two_by_two():
    assert min_path_sum([[1, 2], [1, 1]]) == 3


def test_empty():
    assert min_path_sum([]) == 0
```

`test_classic` has the cheapest route `1 -> 3 -> 1 -> 1 -> 1`, summing to `7`. The single-row and
single-column tests matter because in those grids there's no choice at all: you must walk the whole
line, so the answer is the total. They're the base cases in disguise.

### Try to run the test

Nothing to import yet:

```
ModuleNotFoundError: No module named 'dp_grid.solutions.min_path_sum'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return `0` so the tests run:

```python
from __future__ import annotations


def min_path_sum(grid: list[list[int]]) -> int:
    return 0
```

Run `uv run pytest`:

```
    def test_classic():
        grid = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
>       assert min_path_sum(grid) == 7
E       assert 0 == 7
E        +  where 0 = min_path_sum([[1, 3, 1], [1, 5, 1], [4, 2, 1]])
```

Failing on the value, exactly as we want. `test_empty` passes for the same lucky reason as before.

### Write enough code to make it pass

The base cases need real work this time. The top-left cell is just its own value. The rest of the
first row can only be reached from the left, and the rest of the first column only from above, so
each is a running total. Then every interior cell adds its value to the cheaper of the two
neighbours.

```python
from __future__ import annotations


def min_path_sum(grid: list[list[int]]) -> int:
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = grid[0][0]
    for c in range(1, cols):
        dp[0][c] = dp[0][c - 1] + grid[0][c]
    for r in range(1, rows):
        dp[r][0] = dp[r - 1][0] + grid[r][0]
    for r in range(1, rows):
        for c in range(1, cols):
            dp[r][c] = grid[r][c] + min(dp[r - 1][c], dp[r][c - 1])
    return dp[rows - 1][cols - 1]
```

The tests pass.

Unique Paths could seed the whole table with a single constant; here the first row and first column
each accumulate, so they get their own two loops before the main double loop. That's the difference
between a problem whose base case is a fixed value and one whose base case is itself a tiny
prefix-sum. **When the edges aren't constant, fill them first, then let the interior read from
finished neighbours.**

### Refactor

The shape matches the template (`combine = here + min(up, left)`), with the base case spread across
two edge loops instead of one constant. I considered collapsing the two edge loops into the main
loop with `if r == 0 or c == 0` branches, the way the template does it, but the separate loops read
more plainly and skip a branch on every cell. I'll keep them. Re-run the tests; still green.

## Problem 3: Maximal Square

> Given a grid of `"0"` and `"1"` strings, find the largest square made entirely of `"1"`s and
> return its area.

This one's the reason the template carries a diagonal. We're not walking a path anymore, we're
measuring a 2D shape, and a square's size at a cell depends on three neighbours, not two.

Here's the idea. Let `dp[r][c]` be the side length of the largest all-ones square whose
*bottom-right corner* sits at `(r, c)`. If that cell is a `"1"`, it can extend the squares ending
just above it, just left of it, and on its diagonal. A square of side `k + 1` exists here only if
all three of those neighbours already support a square of side at least `k`, so we take the
*minimum* of the three and add one. The smallest of the three is the bottleneck.

### Write the test first

```python
from maximal_square import maximal_square


def test_classic():
    matrix = [
        ["1", "0", "1", "0", "0"],
        ["1", "0", "1", "1", "1"],
        ["1", "1", "1", "1", "1"],
        ["1", "0", "0", "1", "0"],
    ]
    assert maximal_square(matrix) == 4


def test_single_one():
    assert maximal_square([["0", "1"]]) == 1


def test_all_zeros():
    assert maximal_square([["0", "0"], ["0", "0"]]) == 0


def test_full_square():
    assert maximal_square([["1", "1"], ["1", "1"]]) == 4


def test_single_zero_cell():
    assert maximal_square([["0"]]) == 0


def test_empty():
    assert maximal_square([]) == 0
```

`test_classic` hides a 2-by-2 block of ones, so its area is `4`, not the side length `2`. That gap
between side and area is where a tired solution returns the wrong number, so the test names it.
`test_single_one` checks that a lone `"1"` on the first row counts as a square of side `1`.

### Try to run the test

```
ModuleNotFoundError: No module named 'dp_grid.solutions.maximal_square'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to `0`:

```python
from __future__ import annotations


def maximal_square(matrix: list[list[str]]) -> int:
    return 0
```

Run `uv run pytest`:

```
    def test_classic():
        matrix = [
            ["1", "0", "1", "0", "0"],
            ["1", "0", "1", "1", "1"],
            ["1", "1", "1", "1", "1"],
            ["1", "0", "0", "1", "0"],
        ]
>       assert maximal_square(matrix) == 4
E       AssertionError: assert 0 == 4
E        +  where 0 = maximal_square([['1', '0', '1', '0', '0'], ...])
```

`test_all_zeros`, `test_single_zero_cell`, and `test_empty` pass on the stub because their answer
really is `0`. The three that want a non-zero area fail on the value. Now let's earn those.

### Write enough code to make it pass

Walk the grid. Skip any `"0"` cell, since no square can end there. On a `"1"` in the first row or
column, the best square is just that cell, side `1`. Otherwise take one more than the minimum of
the three neighbours. Track the largest side we see, and return its square.

```python
from __future__ import annotations


def maximal_square(matrix: list[list[str]]) -> int:
    if not matrix or not matrix[0]:
        return 0
    rows, cols = len(matrix), len(matrix[0])
    dp = [[0] * cols for _ in range(rows)]
    best = 0
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] != "1":
                continue
            if r == 0 or c == 0:
                dp[r][c] = 1
            else:
                dp[r][c] = 1 + min(dp[r - 1][c], dp[r][c - 1], dp[r - 1][c - 1])
            best = max(best, dp[r][c])
    return best * best
```

Green.

The `min` of three neighbours is the whole trick. A square ending here is only as big as the
smallest square that meets it from above, the left, and the diagonal, because all three corners
have to be backed by ones. We return `best * best` because the problem wants area, and `dp` stores
side length. That's the conversion `test_classic` was guarding.

### Refactor

This is the template's full form: `base(r, c) = 1` for any `"1"` on an edge, and
`combine = 1 + min(up, left, diag)`, with the `"0"` cells left at their default `0`. It's the first
problem in the chapter that actually uses the diagonal neighbour the template reserved a slot for.
Nothing to simplify; the `continue` keeps the two cases flat and readable. Re-run the tests one
last time.

## Wrapping up

- **Grid DP fills a 2D table top-left to bottom-right, so every cell reads only finished
  neighbours**: above, left, and sometimes the diagonal. That ordering is the invariant the whole
  pattern rests on.
- **The first row and first column are your base cases.** Sometimes they're a constant (Unique
  Paths), sometimes a running total (Minimum Path Sum). Fill them before the interior.
- **The `combine` step is the problem.** `up + left` counts paths, `here + min(up, left)` finds the
  cheapest, and `1 + min(up, left, diag)` measures the largest square. Same walk, different fold.
- **Watch the units.** Maximal Square stores side lengths but returns area, and that off-by-a-square
  is the kind of thing a test should pin down.
