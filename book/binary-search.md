# Binary Search

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/binary_search)**

Binary search is one of the highest-value patterns in interviews: it turns O(n) into O(log n),
and it applies to far more than "find a value in a sorted array". Here's the mental model that
makes it click:

> Binary search finds the **boundary** in a sequence of `False, False, ..., False, True, True,
> ..., True`, the first index where some `feasible(x)` predicate flips to True.

Once you can phrase a problem as "find the first `x` where `feasible(x)` is true", the loop is
always the same.

## When to reach for it

Reach for binary search when one of these holds:

- The search space is **sorted or monotonic**: an array, or an *answer range* where "if `x`
  works, everything bigger works".
- You see "minimum/maximum value such that...", "first/last position of...", or a size constraint
  you can binary-search the answer for.

## The template

```python
from __future__ import annotations

from typing import Callable


def find_first_true(lo: int, hi: int, feasible: Callable[[int], bool]) -> int:
    first_true = hi + 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            first_true = mid
            hi = mid - 1  # look for an even earlier True
        else:
            lo = mid + 1  # True (if any) is to the right
    return first_true
```

Two correctness habits kill the classic bugs:

- Use `while lo <= hi` with `hi = mid - 1` and `lo = mid + 1`. No infinite loops, no off-by-one.
- `mid = (lo + hi) // 2`. In Python there's no integer overflow to worry about, unlike C or Java.

The sentinel `first_true = hi + 1` means "predicate never became true", the conventional
"not found / past the end" answer.

## Problem 1: First Element Not Smaller Than Target (boundary on an array)

> In a sorted array, return the first index with `arr[i] >= target` (the lower-bound insertion
> point, i.e. `bisect_left`). Return `len(arr)` if every element is smaller.

This is the boundary search in its purest form. `feasible(i) = arr[i] >= target` is
`False, ..., False, True, ..., True`, and we want the first True.

### Write the test first

```python
import bisect

import pytest
from hypothesis import given
from hypothesis import strategies as st

from first_not_smaller import first_not_smaller


@pytest.mark.parametrize(
    ("arr", "target", "expected"),
    [
        ([1, 3, 3, 5, 8, 8, 10], 5, 3),
        ([1, 3, 3, 5, 8, 8, 10], 3, 1),  # first of the duplicates
        ([1, 3, 3, 5, 8, 8, 10], 0, 0),  # smaller than everything
        ([1, 3, 3, 5, 8, 8, 10], 11, 7),  # larger than everything -> len(arr)
        ([], 5, 0),  # empty array
        ([2], 2, 0),  # single element, equal
        ([2], 3, 1),  # single element, target larger
    ],
)
def test_first_not_smaller(arr, target, expected):
    assert first_not_smaller(arr, target) == expected
```

The duplicate case (`target == 3`, which appears twice) is the one that pins down "first". A
solution that returns any matching index, rather than the earliest one, gets it wrong.

We also pin it with a **property test** against the standard library. That's a great habit for
binary search, where off-by-ones hide in untested corners:

```python
@given(
    st.lists(st.integers(), max_size=50).map(sorted),
    st.integers(),
)
def test_matches_bisect_left(arr, target):
    assert first_not_smaller(arr, target) == bisect.bisect_left(arr, target)
```

### Try to run the test

We've imported `first_not_smaller` from a module that doesn't define it yet, so the import is
the first thing to break:

```
ImportError: cannot import name 'first_not_smaller' from 'first_not_smaller'
```

No function, nothing to call. Listen to the error: it tells us where to start.

### Write the minimal amount of code for the test to run and check the failing test output

Give it a `first_not_smaller` that returns a stub `0`. We're not solving anything yet. We just
want the test to run so we can watch it fail on the value, which proves the test checks what we
think it does.

```python
from __future__ import annotations


def first_not_smaller(arr: list[int], target: int) -> int:
    return 0
```

Run `uv run pytest`:

```
    def test_first_not_smaller(arr, target, expected):
>       assert first_not_smaller(arr, target) == expected
E       assert 0 == 3
E        +  where 0 = first_not_smaller([1, 3, 3, 5, 8, 8, 10], 5)
```

The test runs and fails on the value, not on a missing name. That's exactly what we want before
writing the real thing. (The empty-array row happens to expect `0`, so it passes by luck. One
green case proves nothing on its own.)

### Write enough code to make it pass

`feasible(i) = arr[i] >= target` drops straight into the boundary template. We track the first
qualifying index and keep pushing `hi` left to find an earlier one:

```python
from __future__ import annotations


def first_not_smaller(arr: list[int], target: int) -> int:
    lo, hi = 0, len(arr) - 1
    first_true = len(arr)  # sentinel: nothing is >= target
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] >= target:
            first_true = mid
            hi = mid - 1  # look for an earlier qualifying index
        else:
            lo = mid + 1
    return first_true
```

Run the tests again and they're green, property test included.

The sentinel starts at `len(arr)`, not `len(arr) - 1`. When nothing is `>= target` (including the
empty array, where the loop never runs), that's the answer `bisect_left` gives too: the insertion
point past the end.

### Refactor

There's little to tidy in a dozen lines, but it's worth naming the shape. This *is*
`find_first_true` from the template, with `feasible` inlined as `arr[mid] >= target` and the
sentinel set to `len(arr)`. Re-run the tests to confirm nothing moved.

> In real interviews, reach for `bisect.bisect_left` and `bisect_right`: Python's batteries.
> Knowing how to write it by hand is what they're testing, and knowing the built-in is what they
> want you to use day to day.

## Problem 2: Search in Rotated Sorted Array (binary search with a twist)

> A sorted array rotated at an unknown pivot, e.g. `[4, 5, 6, 7, 0, 1, 2]`. Find a target's
> index, or `-1`.

The array isn't fully sorted any more, so the plain boundary template doesn't apply directly.
But there's structure to exploit, which we'll get to once we have a failing test.

### Write the test first

```python
import pytest

from search_rotated import search


@pytest.mark.parametrize(
    ("nums", "target", "expected"),
    [
        ([4, 5, 6, 7, 0, 1, 2], 0, 4),
        ([4, 5, 6, 7, 0, 1, 2], 3, -1),
        ([4, 5, 6, 7, 0, 1, 2], 4, 0),  # pivot element
        ([4, 5, 6, 7, 0, 1, 2], 2, 6),  # last element
        ([1], 1, 0),
        ([1], 0, -1),
        ([], 5, -1),  # empty
        ([5, 1, 3], 3, 2),  # small rotation
    ],
)
def test_search_rotated(nums, target, expected):
    assert search(nums, target) == expected
```

We add a second test that cross-checks against the obvious O(n) scan for every value in a known
rotation. If the clever version ever disagrees with the dumb one, the clever version is wrong:

```python
def test_agrees_with_linear_scan_on_a_rotation():
    base = [10, 20, 30, 40, 50]
    rotated = [30, 40, 50, 10, 20]
    for value in base:
        assert search(rotated, value) == rotated.index(value)
```

### Try to run the test

The function doesn't exist yet, so the import is what fails first:

```
ImportError: cannot import name 'search' from 'search_rotated'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub `search` to return `-1` so the tests run:

```python
from __future__ import annotations


def search(nums: list[int], target: int) -> int:
    return -1
```

Run `uv run pytest`:

```
    def test_search_rotated(nums, target, expected):
>       assert search(nums, target) == expected
E       assert -1 == 4
E        +  where -1 = search([4, 5, 6, 7, 0, 1, 2], 0)
```

The "not found" rows pass because `-1` is what they expect, and the rest fail on the value. Now
let's make them all pass for the right reason.

### Write enough code to make it pass

The key insight: at any `mid`, **at least one half is fully sorted**. Detect which half, check
whether the target lies inside that sorted half, and discard the other:

```python
from __future__ import annotations


def search(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:  # left half [lo..mid] is sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:  # right half [mid..hi] is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
```

The tests pass, linear-scan cross-check included.

The comparison `nums[lo] <= nums[mid]` is what tells us the left half is sorted. Once we know one
half is sorted, the bounds check `nums[lo] <= target < nums[mid]` is an ordinary range test, and
we can confidently throw away the half that can't contain the target. We still halve the search
each step, so it's O(log n).

### Refactor

The structure is already as flat as it gets, two nested `if`s mirroring each other. The thing
worth naming is that this is still a binary search: every iteration discards half the array. We've
swapped the simple `feasible` predicate for a "which half is sorted, and is the target in it"
decision, but the halving discipline is the same. Re-run the tests.

## Problem 3: Integer Square Root (binary search on the *answer*)

> Return `floor(sqrt(n))` without using `math.sqrt`.

This is the one that shows binary search isn't about arrays at all. We search the **answer space**
`[0, n]` for the largest `x` with `x * x <= n`. Here `feasible(x) = x * x <= n` runs
`True, ..., True, False`, so we want the *last* True rather than the first.

### Write the test first

```python
import math

import pytest
from hypothesis import given
from hypothesis import strategies as st

from sqrt import int_sqrt


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (0, 0),
        (1, 1),
        (4, 2),
        (8, 2),  # floor(2.82...)
        (9, 3),
        (15, 3),
        (16, 4),
        (2, 1),
    ],
)
def test_int_sqrt(n, expected):
    assert int_sqrt(n) == expected


def test_negative_raises():
    with pytest.raises(ValueError):
        int_sqrt(-1)


@given(st.integers(min_value=0, max_value=10**12))
def test_matches_math_isqrt(n):
    assert int_sqrt(n) == math.isqrt(n)
```

The non-perfect squares (`8` and `15`) are the cases that earn their keep: they force the *floor*
behaviour, not just exact roots. The property test then leans on `math.isqrt` to cover everything
up to a trillion.

### Try to run the test

Nothing to import yet:

```
ImportError: cannot import name 'int_sqrt' from 'sqrt'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return `0` so the tests run:

```python
from __future__ import annotations


def int_sqrt(n: int) -> int:
    return 0
```

Run `uv run pytest`:

```
    def test_int_sqrt(n, expected):
>       assert int_sqrt(n) == expected
E       assert 0 == 1
E        +  where 0 = int_sqrt(1)
```

Failing on the values, as expected. The `(0, 0)` row passes by luck, and `test_negative_raises`
fails because our stub never raises. Good, that's the failing test we want.

### Write enough code to make it pass

Search the answer range for the largest `x` with `x * x <= n`. We track the last `x` that
satisfied the predicate and keep pushing `lo` right to do better:

```python
from __future__ import annotations


def int_sqrt(n: int) -> int:
    if n < 0:
        raise ValueError("square root is undefined for negative numbers")
    if n < 2:
        return n
    lo, hi = 1, n // 2
    answer = 1  # last x known to satisfy x*x <= n
    while lo <= hi:
        mid = (lo + hi) // 2
        if mid * mid <= n:
            answer = mid
            lo = mid + 1  # try to do better
        else:
            hi = mid - 1
    return answer
```

Green, property test and all.

Same skeleton as before, but the "array" is the range of candidate answers and `feasible` is
`mid * mid <= n`. The early `n < 2` return handles `0` and `1` (where `n // 2` would give an
empty range), and the negative check raises before we start.

### Refactor

There's nothing to tidy in the loop, but notice what changed from Problem 1. There we wanted the
*first* True, so we saved on a hit and moved `hi` left. Here we want the *last* True, so we save
on a hit and move `lo` right. Same five-line skeleton, mirror-image bookkeeping. That symmetry is
the whole pattern: this "binary search the answer" trick solves a huge family of problems, like
minimum capacity, minimum eating speed, smallest divisor, and more. Re-run the tests.

## Wrapping up

- Model binary search as **"find the boundary where `feasible(x)` flips"**. It generalises far
  beyond sorted-array lookup.
- Use `while lo <= hi`, `hi = mid - 1` and `lo = mid + 1`. Python has no integer overflow.
- **Binary search the answer space**, not just arrays, for min/max-feasible-value problems.
- Reach for `bisect` in practice, and pin your hand-written versions with **property tests**
  against `bisect` and `math.isqrt`.
