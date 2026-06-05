# Intervals

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/intervals)**

An interval is a `[start, end]` pair, and almost every interval problem is the same move wearing
a different hat: sort by start, then sweep once. The reusable skeleton lives in
[`intervals/_template.py`](intervals/_template.py), and we build three worked problems test-first
in `intervals/solutions/`.

## When to reach for sort-then-sweep

You're handed a pile of intervals in no particular order and asked something about how they
overlap. The brute-force instinct is to compare every pair, which is O(n²). Sorting first
collapses that to one pass. Reach for it when:

- You need to **merge or combine overlapping intervals**, or count the distinct blocks they form.
- You need to know **whether any two overlap** (meeting rooms, double-bookings, conflicts).
- You're inserting or removing one interval and need to **re-merge the neighbourhood**.

The whole reason sorting helps: once the intervals are ordered by start, the only interval that
can overlap the one you're currently holding is the *next* one. You never have to look backwards.
That's what turns the O(n²) pair scan into a single left-to-right sweep.

## The template

```python
def merge_sorted(intervals):
    if not intervals:
        return []

    ordered = sorted(intervals, key=lambda interval: interval[0])
    merged = [list(ordered[0])]
    for start, end in ordered[1:]:
        last = merged[-1]
        if start <= last[1]:
            last[1] = max(last[1], end)
        else:
            merged.append([start, end])
    return merged
```

We sort by start, seed `merged` with a copy of the first interval, then walk the rest. `last` is
the interval we're currently holding open. For each new `[start, end]` we ask one question: does
it overlap the open one? Because the list is start-sorted, that question is just `start <= last[1]`.
If yes, we stretch the open interval's end (the `max` matters, more on that below). If no, there's
a gap, so we close the open interval and push a fresh one.

The *invariant* is that `merged` only ever holds non-overlapping intervals, in order, and the last
one is the only one still "open" for extension. Everything in this chapter is a variation on this
sweep.

One detail worth pinning down now: I copy the first interval with `list(ordered[0])` instead of
reusing it. We mutate `last[1]` in place as we extend, and mutating the caller's input is the kind
of thing that bites you two problems later. Copy on the way in.

## Problem 1: Merge Intervals

> Given a list of `[start, end]` intervals, merge all the overlapping ones and return the
> non-overlapping result.

This is the template in its purest form, so let's write it out properly and let the tests pin down
the edge cases.

### Write the test first

```python
from .merge_intervals import merge


def test_overlapping_pair():
    assert merge([[1, 3], [2, 6]]) == [[1, 6]]


def test_touching_intervals_merge():
    assert merge([[1, 4], [4, 5]]) == [[1, 5]]


def test_disjoint_intervals_stay_separate():
    assert merge([[1, 2], [5, 6]]) == [[1, 2], [5, 6]]


def test_unsorted_input():
    assert merge([[2, 6], [1, 3], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]


def test_interval_swallowed_by_a_wider_one():
    assert merge([[1, 10], [2, 4], [5, 6]]) == [[1, 10]]
```

Two of these carry their weight. `test_touching_intervals_merge` decides a policy question: do
`[1, 4]` and `[4, 5]` count as overlapping? We're saying yes, they touch at `4`, so they merge.
And `test_interval_swallowed_by_a_wider_one` is the case a naive solution gets wrong: after `[1, 10]`
opens, `[2, 4]` sits entirely inside it, so the end must *not* shrink to `4`. That's the `max`.

I'll also add an empty-list test, because a function that walks `ordered[1:]` needs to survive an
empty input:

```python
def test_empty():
    assert merge([]) == []
```

### Try to run the test

The module doesn't define `merge` yet, so the import is the first thing to break:

```
ImportError: cannot import name 'merge' from 'intervals.solutions.merge_intervals'
```

No function, nothing to call. The error is pointing right at where we start.

### Write the minimal amount of code for the test to run and check the failing test output

Give it a `merge` that always returns an empty list. It's wrong on purpose. We want the test to
*run* so we can watch it fail on the value, which proves the test is actually checking something.

```python
from __future__ import annotations


def merge(intervals: list[list[int]]) -> list[list[int]]:
    return []
```

Run `uv run pytest`:

```
    def test_overlapping_pair():
>       assert merge([[1, 3], [2, 6]]) == [[1, 6]]
E       assert [] == [[1, 6]]
E
E         Right contains one more item: [1, 6]
```

The test runs and fails on the value, not on a missing name. (Notice `test_empty` already passes:
our stub returns `[]`, which happens to be the right answer for the empty case. One green test
proves nothing on its own.)

### Write enough code to make it pass

Now the real thing, which is the template with concrete types:

```python
from __future__ import annotations


def merge(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    ordered = sorted(intervals, key=lambda interval: interval[0])
    merged = [list(ordered[0])]
    for start, end in ordered[1:]:
        last = merged[-1]
        if start <= last[1]:
            last[1] = max(last[1], end)
        else:
            merged.append([start, end])
    return merged
```

Run the tests and they're green.

The `sorted` call is what makes `test_unsorted_input` pass without any extra work: we never assume
the caller handed us sorted intervals, we sort them ourselves. And `start <= last[1]` (with `<=`,
not `<`) is what makes touching intervals merge, satisfying `test_touching_intervals_merge`.

### Refactor

There's nothing to tidy in the algorithm, it's the same shape as `merge_sorted` from the template.
The one thing worth naming is the cost: the sweep is O(n), but the `sorted` call dominates, so the
whole thing is O(n log n). You can't do better than `n log n` here, because if you could merge
intervals faster you could sort numbers faster, and you can't. Re-run the tests to confirm nothing
moved.

## Problem 2: Insert Interval

> Given a list of non-overlapping intervals already sorted by start, insert a new interval and
> merge anything it now overlaps.

Here's the twist: the input is *already sorted*. Calling `sorted` again would throw away that gift
and pay O(n log n) for nothing. When the data is pre-sorted, the sweep alone is O(n), so let's not
re-sort. We walk the list in three phases instead.

### Write the test first

```python
from .insert_interval import insert


def test_insert_into_gap():
    assert insert([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]


def test_insert_overlapping_several():
    assert insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == [
        [1, 2],
        [3, 10],
        [12, 16],
    ]


def test_insert_into_empty():
    assert insert([], [5, 7]) == [[5, 7]]


def test_insert_before_everything():
    assert insert([[3, 5], [8, 10]], [1, 2]) == [[1, 2], [3, 5], [8, 10]]


def test_insert_after_everything():
    assert insert([[1, 2], [3, 5]], [8, 10]) == [[1, 2], [3, 5], [8, 10]]


def test_insert_touching_neighbours_merges_them():
    assert insert([[1, 2], [5, 6]], [2, 5]) == [[1, 6]]
```

`test_insert_overlapping_several` is the headline case: `[4, 8]` swallows three middle intervals
and fuses them into `[3, 10]`. And `test_insert_touching_neighbours_merges_them` is sneaky: the new
`[2, 5]` touches `[1, 2]` on its left and `[5, 6]` on its right, so all three collapse into one.
A solution that only merges on one side gets that wrong.

### Try to run the test

```
ImportError: cannot import name 'insert' from 'intervals.solutions.insert_interval'
```

Same starting point as before: the function doesn't exist.

### Write the minimal amount of code for the test to run and check the failing test output

Stub `insert` to return an empty list so the tests run and fail on the value:

```python
from __future__ import annotations


def insert(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:
    return []
```

Run `uv run pytest`:

```
    def test_insert_into_gap():
>       assert insert([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]
E       assert [] == [[1, 5], [6, 9]]
E
E         Right contains 2 more items, first extra item: [1, 5]
```

All six fail on the value. Good, now they can only go green for the right reason.

### Write enough code to make it pass

Three phases, no sorting. First copy every interval that ends strictly before the new one starts
(those are untouched, to the left). Then absorb every interval that overlaps the new one, widening
`start` and `end` as we go, and push the widened interval once. Finally copy whatever's left.

```python
from __future__ import annotations


def insert(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:
    start, end = new_interval
    result: list[list[int]] = []
    i = 0
    n = len(intervals)

    while i < n and intervals[i][1] < start:
        result.append(intervals[i])
        i += 1

    while i < n and intervals[i][0] <= end:
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    result.append([start, end])

    while i < n:
        result.append(intervals[i])
        i += 1

    return result
```

The tests pass.

The middle loop is where the merging happens. We widen `start` and `end` to cover everything the
new interval touches, *then* append the result once. That single append after a loop of widening is
what makes `test_insert_overlapping_several` collapse three intervals into one and what merges both
neighbours in `test_insert_touching_neighbours_merges_them`. The `<` in the first loop versus the
`<=` in the second is deliberate: an interval ending exactly at `start` should merge (touching
counts), so it belongs to the second phase, not the first.

### Refactor

No change to the code, but notice what we bought by not sorting. Each interval is visited by
exactly one of the three loops, so this is a clean O(n) pass. Merge Intervals had to sort and paid
O(n log n); Insert Interval gets the data pre-sorted and stays linear. **When the input is already
sorted, don't re-sort, sweep.** Re-run the tests.

## Problem 3: Meeting Rooms

> Given a list of meeting time intervals, can one person attend every meeting? They can as long as
> no two meetings overlap.

We don't need to merge anything here, we just need to detect a single collision. Same sort, simpler
sweep: compare each meeting to the one before it.

### Write the test first

```python
from .can_attend_meetings import can_attend_meetings


def test_overlapping_meetings_cannot_all_be_attended():
    assert can_attend_meetings([[0, 30], [5, 10], [15, 20]]) is False


def test_disjoint_meetings_can_all_be_attended():
    assert can_attend_meetings([[7, 10], [2, 4]]) is True


def test_touching_meetings_are_fine():
    assert can_attend_meetings([[1, 5], [5, 8]]) is True


def test_no_meetings():
    assert can_attend_meetings([]) is True


def test_single_meeting():
    assert can_attend_meetings([[4, 9]]) is True
```

Notice `test_touching_meetings_are_fine` flips the policy from Problem 1. When we *merged*
intervals, touching at a point meant overlap. For meetings, a meeting that ends at `5` and another
that starts at `5` are back-to-back, not a clash, so touching is fine here. The boundary case is
the same numbers; the right answer depends on what the problem actually asks. Read the prompt, don't
assume.

### Try to run the test

```
ImportError: cannot import name 'can_attend_meetings' from 'intervals.solutions.can_attend_meetings'
```

The function isn't there yet.

### Write the minimal amount of code for the test to run and check the failing test output

This one needs care. The stub can't return a blanket `False`, because four of the five tests expect
`True`, so a `False` stub would pass nothing useful and a `True` stub would pass four by luck. I'll
return `True`, which makes the failure land on exactly the one case that matters, the actual
overlap:

```python
from __future__ import annotations


def can_attend_meetings(intervals: list[list[int]]) -> bool:
    return True
```

Run `uv run pytest`:

```
    def test_overlapping_meetings_cannot_all_be_attended():
>       assert can_attend_meetings([[0, 30], [5, 10], [15, 20]]) is False
E       assert True is False
E        +  where True = can_attend_meetings([[0, 30], [5, 10], [15, 20]])

1 failed, 4 passed
```

The four `True` cases pass because the stub returns `True`, which is the right answer for them but
for the wrong reason: the stub doesn't look at the meetings at all. The one that fails is the only
one with a real overlap, and it's the behaviour we still have to build. That's the failing test
guiding us to the work that's left.

### Write enough code to make it pass

Sort by start, then walk adjacent pairs. If a later meeting starts before the earlier one ends, they
collide:

```python
from __future__ import annotations


def can_attend_meetings(intervals: list[list[int]]) -> bool:
    ordered = sorted(intervals, key=lambda interval: interval[0])
    for earlier, later in zip(ordered, ordered[1:]):
        if later[0] < earlier[1]:
            return False
    return True
```

Green.

`zip(ordered, ordered[1:])` pairs each meeting with its successor, which is a tidy way to sweep
adjacent pairs without juggling indices. The comparison is `later[0] < earlier[1]` with a strict
`<`, so a meeting that starts exactly when the previous one ends does *not* count as a clash, which
is what `test_touching_meetings_are_fine` demanded. Empty and single-meeting inputs produce no pairs,
so the loop never runs and we fall through to `True`, covering `test_no_meetings` and
`test_single_meeting` for free.

### Refactor

The code's already small, so the refactor is about seeing the family resemblance. All three problems
sorted by start and swept once. Merge built up a result, Insert widened a window, Meeting Rooms just
checked a condition and bailed early. The sort is the expensive part every time (O(n log n)); the
sweep is always O(n). Once you see the sort-then-sweep skeleton, these stop being three problems and
become one. Re-run the tests.

## Wrapping up

- **Sort by start, then sweep once.** Sorting guarantees the only interval that can overlap your
  current one is the next, which turns an O(n²) pair scan into an O(n log n) sort plus an O(n) walk.
- **The merge skeleton is the core move**: hold one open interval, extend it on overlap
  (`start <= last[1]`), close it and open a new one on a gap. Use `max` when extending so a swallowed
  interval doesn't shrink the end.
- **Whether touching counts as overlap is a policy decision, not a fact.** Merge Intervals merges on
  touch (`<=`); Meeting Rooms treats back-to-back as fine (`<`). Read the prompt.
- **When the input is already sorted, don't re-sort.** Insert Interval stays O(n) by sweeping in
  three phases instead of paying for another sort.

Next: [Interval DP](dp-intervals.md), where instead of sweeping intervals left to right you build
answers up from smaller sub-intervals.
