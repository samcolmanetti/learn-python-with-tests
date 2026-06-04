# Binary Search

**[You can find all the code for this chapter here](binary_search/)**

Binary search is the highest-leverage pattern in interviews: it turns O(n) into O(log n), and it
applies to far more than "find a value in a sorted array". The mental model that unlocks it:

> Binary search finds the **boundary** in a sequence of `False, False, …, False, True, True, …,
> True` — the first index where some `feasible(x)` predicate flips to True.

Once you can phrase a problem as "find the first `x` where `feasible(x)` is true", the loop is
always the same.

## When to reach for it

- The search space is **sorted or monotonic** — an array, or an *answer range* where "if `x`
  works, everything bigger works".
- You see "minimum/maximum value such that…", "first/last position of…", or a size constraint
  you can binary-search the answer for.

## The template

```python
def find_first_true(lo, hi, feasible):
    first_true = hi + 1            # sentinel: predicate never true
    while lo <= hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            first_true = mid
            hi = mid - 1           # a smaller answer might also work
        else:
            lo = mid + 1           # need to go bigger
    return first_true
```

Two correctness habits that kill the classic bugs:

- Use `while lo <= hi` with `hi = mid - 1` / `lo = mid + 1` (no infinite loops, no off-by-one).
- `mid = (lo + hi) // 2` — in Python there's no integer overflow to worry about, unlike C/Java.

## Problem 1: First Element Not Smaller Than Target (boundary on an array)

> In a sorted array, return the first index with `arr[i] >= target` (i.e. `bisect_left`).

### Write the test first

```python
@pytest.mark.parametrize(
    ("arr", "target", "expected"),
    [
        ([1, 3, 3, 5, 8, 8, 10], 5, 3),
        ([1, 3, 3, 5, 8, 8, 10], 3, 1),   # first of the duplicates
        ([1, 3, 3, 5, 8, 8, 10], 11, 7),  # larger than everything -> len(arr)
        ([], 5, 0),
    ],
)
def test_first_not_smaller(arr, target, expected):
    assert first_not_smaller(arr, target) == expected
```

We also pin it with a **property test** against the standard library — a great habit for binary
search, where off-by-ones hide in untested corners:

```python
@given(st.lists(st.integers(), max_size=50).map(sorted), st.integers())
def test_matches_bisect_left(arr, target):
    assert first_not_smaller(arr, target) == bisect.bisect_left(arr, target)
```

### Make it pass

`feasible(i) = arr[i] >= target` is exactly the boundary template:

```python
def first_not_smaller(arr, target):
    lo, hi = 0, len(arr) - 1
    first_true = len(arr)
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] >= target:
            first_true = mid
            hi = mid - 1
        else:
            lo = mid + 1
    return first_true
```

> In real interviews, reach for `bisect.bisect_left` / `bisect_right` — Python's batteries.
> Knowing how to write it by hand is what they're testing; knowing the built-in is what they
> want you to use day to day.

## Problem 2: Search in Rotated Sorted Array (binary search with a twist)

> A sorted array rotated at an unknown pivot, e.g. `[4, 5, 6, 7, 0, 1, 2]`. Find a target's
> index, or `-1`.

### Write the test first

```python
@pytest.mark.parametrize(
    ("nums", "target", "expected"),
    [
        ([4, 5, 6, 7, 0, 1, 2], 0, 4),
        ([4, 5, 6, 7, 0, 1, 2], 3, -1),
        ([4, 5, 6, 7, 0, 1, 2], 4, 0),   # pivot
        ([1], 0, -1),
        ([], 5, -1),
    ],
)
def test_search_rotated(nums, target, expected):
    assert search(nums, target) == expected
```

### Make it pass

The key insight: at any `mid`, **at least one half is fully sorted**. Detect which, check if the
target lies within that sorted half, and discard the other.

```python
def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:                 # left half sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                                     # right half sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
```

## Problem 3: Integer Square Root (binary search on the *answer*)

> Return `floor(sqrt(n))` without `math.sqrt`.

This is the one that shows binary search isn't about arrays at all. We search the **answer
space** `[0, n]` for the largest `x` with `x * x <= n`.

### Write the test first

```python
@pytest.mark.parametrize(
    ("n", "expected"),
    [(0, 0), (1, 1), (4, 2), (8, 2), (9, 3), (15, 3), (16, 4)],
)
def test_int_sqrt(n, expected):
    assert int_sqrt(n) == expected


@given(st.integers(min_value=0, max_value=10**12))
def test_matches_math_isqrt(n):
    assert int_sqrt(n) == math.isqrt(n)
```

### Make it pass

```python
def int_sqrt(n):
    if n < 0:
        raise ValueError("square root is undefined for negative numbers")
    if n < 2:
        return n
    lo, hi = 1, n // 2
    answer = 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if mid * mid <= n:
            answer = mid
            lo = mid + 1   # try for a bigger root
        else:
            hi = mid - 1
    return answer
```

Same skeleton, but the "array" is the range of candidate answers and `feasible` is `mid*mid <=
n`. This "binary search the answer" trick solves a huge family of problems: minimum capacity,
minimum eating speed, smallest divisor, and more.

## Wrapping up

- Model binary search as **"find the boundary where `feasible(x)` flips"** — it generalises far
  beyond sorted-array lookup.
- Use `while lo <= hi`, `hi = mid - 1` / `lo = mid + 1`; Python has no integer overflow.
- **Binary search the answer space**, not just arrays, for min/max-feasible-value problems.
- Reach for `bisect` in practice; pin your hand-written versions with **property tests** against
  `bisect` / `math.isqrt`.

Next: [Prefix Sum](prefix-sum.md).
