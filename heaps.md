# Heaps

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/heaps)**

A heap is an **interview pattern** for one job: keep the smallest (or largest) thing reachable in
O(log n) while items come and go. Python's `heapq` gives you that as a plain list, and a handful of
worked problems in [`heaps/solutions/`](heaps/solutions/) reuse the same two or three moves.

## When to reach for a heap

You don't always need the whole thing sorted. Often you only need the extreme: the smallest, the
largest, the `k` best. Sorting is O(n log n) and gives you everything; a heap gives you just the
edge you asked for and lets you stream new items in. Reach for a heap when:

- You want the **top `k`** of something, and `k` is much smaller than `n`. Keep a heap of size `k`
  and the answer falls out in O(n log k), beating a full O(n log n) sort.
- Items **arrive over time** and you need the current min or max after each one. A heap re-finds the
  extreme in O(log n) per insert, where re-sorting would be O(n log n) every time.
- You're **merging several sorted sequences** and always want the next-smallest head across all of
  them.

## The template

`heapq` doesn't give you a `Heap` class. It gives you functions that treat a normal list as a binary
*min-heap*: the smallest element is always at index `0`, `heappush` adds in O(log n), and `heappop`
removes that smallest in O(log n). Here are the two helpers every problem below leans on.

```python
from __future__ import annotations

import heapq
from collections.abc import Iterable


def smallest_n(items: Iterable[float], n: int) -> list[float]:
    """Return the `n` smallest items, smallest first, using a min-heap."""
    heap = list(items)
    heapq.heapify(heap)
    return [heapq.heappop(heap) for _ in range(min(n, len(heap)))]


def largest_n(items: Iterable[float], n: int) -> list[float]:
    """Return the `n` largest items, largest first, by pushing negated values."""
    heap = [-item for item in items]
    heapq.heapify(heap)
    return [-heapq.heappop(heap) for _ in range(min(n, len(heap)))]
```

`heapify` rearranges a list into heap order in one O(n) pass, which is cheaper than pushing items
one at a time. After that, popping repeatedly hands them back smallest-first.

The thing worth memorising is `largest_n`. The standard library has **no max-heap**. The trick is to
*negate on the way in and negate again on the way out*: a min-heap of `-x` is a max-heap of `x`. We
push `-item`, pop the smallest negative (which is the largest original), and flip its sign back.
Every "largest" problem in this chapter is really a min-heap wearing a minus sign.

## Problem 1: Kth Largest Element

> Given an unsorted array of integers, return the `k`th largest element. Duplicates count by
> position, so in `[3, 2, 1, 5, 6, 4]` the 2nd largest is `5`.

The lazy answer is `sorted(nums)[-k]`, which is O(n log n). We can do better. If we keep only the
`k` largest values we've seen so far in a min-heap of size `k`, the smallest of those (the heap's
top) is exactly the `k`th largest. New items either knock out the current weakest or get dropped.

### Write the test first

```python
from .kth_largest_element import find_kth_largest


def test_kth_largest_in_unsorted():
    assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5


def test_with_duplicates():
    assert find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4


def test_largest_is_first():
    assert find_kth_largest([7, 7, 7], 1) == 7


def test_kth_equals_length():
    assert find_kth_largest([3, 2, 1, 5, 6, 4], 6) == 1


def test_handles_negatives():
    assert find_kth_largest([-1, -5, -3, -2], 2) == -2
```

`test_with_duplicates` is the one that pins the behaviour down: duplicates are not deduplicated, so
the 4th largest of that array is `4`, not some distinct-values answer. `test_kth_equals_length` (the
`k`th largest where `k == n` is the minimum) catches off-by-one mistakes at the far end.

### Try to run the test

We've imported `find_kth_largest` from a module that doesn't define it yet, so the import is the
first thing to break:

```
ImportError: cannot import name 'find_kth_largest' from 'heaps.solutions.kth_largest_element'
```

No function, nothing to call. The error is telling us where to start.

### Write the minimal amount of code for the test to run and check the failing test output

Give it a `find_kth_largest` that returns a stub `0`. We're not solving anything yet. We just want
the test to run so we can watch it fail on the value, which proves the test checks what we think it
does.

```python
from __future__ import annotations


def find_kth_largest(nums: list[int], k: int) -> int:
    return 0
```

Run `uv run pytest`:

```
    def test_kth_largest_in_unsorted():
>       assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
E       assert 0 == 5
E        +  where 0 = find_kth_largest([3, 2, 1, 5, 6, 4], 2)
```

It runs and fails on the value, not on a missing name. That's exactly what we want before writing
the real thing.

### Write enough code to make it pass

Push every number onto the heap, but the moment the heap grows past `k`, pop the smallest. What's
left is the `k` largest values, and the smallest of those (at index `0`) is the answer.

```python
from __future__ import annotations

import heapq


def find_kth_largest(nums: list[int], k: int) -> int:
    heap: list[int] = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]
```

Run the tests again and they're green.

This is a min-heap of size `k`, and `heap[0]` is its smallest member: the `k`th largest overall.
Each push and pop is O(log k), and we do it `n` times, so the whole thing is O(n log k). When `k` is
small that beats sorting handily, and we never hold more than `k` items in memory.

### Refactor

There's little to tidy in eight lines, so the refactor here is naming the shape rather than moving
code. Notice we didn't use `largest_n` from the template even though this is a "largest" problem.
That helper materialises all the largest values; here we only ever need one of them, so a bounded
min-heap is the tighter fit. Same family, different size. Re-run the tests to confirm nothing moved.

## Problem 2: Top K Frequent Elements

> Return the `k` most frequent values in an array, most frequent first.

Two steps hide in here. First, count how often each value appears. Second, pull the `k` biggest
counts. Counting is a job for `collections.Counter`, and "the `k` biggest" is the bounded-heap move
we just used, keyed on frequency this time instead of value.

### Write the test first

```python
from .top_k_frequent import top_k_frequent


def test_two_most_frequent():
    assert top_k_frequent([1, 1, 1, 2, 2, 3], 2) == [1, 2]


def test_single_element():
    assert top_k_frequent([1], 1) == [1]


def test_all_distinct_k_equals_length():
    assert sorted(top_k_frequent([5, 6, 7], 3)) == [5, 6, 7]


def test_most_frequent_first():
    assert top_k_frequent([4, 4, 4, 9, 9, 1], 1) == [4]


def test_handles_negatives():
    assert top_k_frequent([-1, -1, -2, -2, -2, 3], 2) == [-2, -1]
```

`test_handles_negatives` does double duty: it checks we count negative values fine, and it checks
order, because `-2` appears three times and `-1` twice, so the result must be `[-2, -1]` and not the
other way round. When every value is distinct (`test_all_distinct_k_equals_length`) the ties make
order arbitrary, so that test sorts before comparing.

### Try to run the test

The function doesn't exist yet, so the import is what fails first:

```
ImportError: cannot import name 'top_k_frequent' from 'heaps.solutions.top_k_frequent'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return an empty list so the tests run:

```python
from __future__ import annotations


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    return []
```

Run `uv run pytest`:

```
    def test_two_most_frequent():
>       assert top_k_frequent([1, 1, 1, 2, 2, 3], 2) == [1, 2]
E       assert [] == [1, 2]
E         
E         Right contains 2 more items, first extra item: 1
```

Failing on the value, as we wanted. Now make it real.

### Write enough code to make it pass

Count with `Counter`, then push `(freq, value)` pairs onto a min-heap and keep only the top `k` by
popping whenever the heap overflows. Popping in order gives smallest frequency first, so we reverse
to put the most frequent at the front.

```python
from __future__ import annotations

import heapq
from collections import Counter


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    counts = Counter(nums)
    heap: list[tuple[int, int]] = []
    for value, freq in counts.items():
        heapq.heappush(heap, (freq, value))
        if len(heap) > k:
            heapq.heappop(heap)
    result = [heapq.heappop(heap)[1] for _ in range(len(heap))]
    result.reverse()
    return result
```

The tests pass.

We push tuples, and `heapq` compares tuples element by element, so `(freq, value)` orders by
frequency first. That's deliberate: the heap's top is always the *least* frequent of the `k` we're
keeping, which is exactly the one to evict when a more frequent value shows up. The final list comes
out least-frequent-first because that's pop order, hence the `reverse()`. Counting is O(n), and the
heap work is O(m log k) where `m` is the number of distinct values.

### Refactor

The body is already tight. The one thing worth pulling out is *why we tupled `(freq, value)` and not
`(value, freq)`*: the heap has to order on frequency, and the first element of the tuple wins the
comparison, so frequency has to come first. Swap the order and you'd build a heap of the rarest
values, which is the opposite problem. Re-run the tests; nothing should move.

## Problem 3: K Closest Points to Origin

> Given a list of `[x, y]` points, return the `k` closest to the origin `(0, 0)`. Any order is
> fine.

"Closest" means smallest distance, and "the `k` smallest" sounds like a min-heap. But watch the
twist: if we keep a heap of size `k` and want to *evict the worst* each time, the worst is the
**farthest** of our current best, so the heap needs the farthest on top. That's a max-heap, and we
build a max-heap by negating. This is the template's `largest_n` trick applied to distance.

One more shortcut: we never need the actual distance, only its ordering. The square root is
monotonic, so comparing `x*x + y*y` ranks points the same as comparing `sqrt(x*x + y*y)`, with no
floating-point error. We compare squared distances and keep everything in integers.

### Write the test first

```python
from .k_closest_points_to_origin import k_closest


def sorted_points(points):
    return sorted(sorted(p) for p in points)


def test_single_closest():
    result = k_closest([[1, 3], [-2, 2]], 1)
    assert sorted_points(result) == [[-2, 2]]


def test_two_closest_ignores_order():
    result = k_closest([[3, 3], [5, -1], [-2, 4]], 2)
    assert sorted_points(result) == sorted_points([[3, 3], [-2, 4]])


def test_k_equals_length_returns_all():
    result = k_closest([[1, 1], [2, 2], [3, 3]], 3)
    assert sorted_points(result) == [[1, 1], [2, 2], [3, 3]]


def test_origin_point_is_closest():
    result = k_closest([[0, 0], [4, 4], [1, 0]], 2)
    assert sorted_points(result) == sorted_points([[0, 0], [1, 0]])


def test_ties_in_distance():
    result = k_closest([[1, 0], [0, 1], [2, 2]], 2)
    assert sorted_points(result) == sorted_points([[1, 0], [0, 1]])
```

The problem says order doesn't matter, so the tests must not depend on it. That's what
`sorted_points` is for: it normalises both sides before comparing, so a correct answer in any order
still passes. `test_ties_in_distance` makes the point that `[1, 0]` and `[0, 1]` are the same
distance from the origin and both have to come back.

### Try to run the test

Nothing to import yet:

```
ImportError: cannot import name 'k_closest' from 'heaps.solutions.k_closest_points_to_origin'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return an empty list so the tests run:

```python
from __future__ import annotations


def k_closest(points: list[list[int]], k: int) -> list[list[int]]:
    return []
```

Run `uv run pytest`:

```
    def test_single_closest():
        result = k_closest([[1, 3], [-2, 2]], 1)
>       assert sorted_points(result) == [[-2, 2]]
E       assert [] == [[-2, 2]]
E         
E         Right contains one more item: [-2, 2]
```

The test runs and fails on the value. Good, the harness works. Now the real thing.

### Write enough code to make it pass

Push `(-distance, point)` so the heap is a max-heap on distance, and drop the farthest whenever the
heap exceeds `k`. Whatever survives is the `k` closest.

```python
from __future__ import annotations

import heapq


def k_closest(points: list[list[int]], k: int) -> list[list[int]]:
    heap: list[tuple[int, list[int]]] = []
    for x, y in points:
        distance = x * x + y * y
        heapq.heappush(heap, (-distance, [x, y]))
        if len(heap) > k:
            heapq.heappop(heap)
    return [point for _, point in heap]
```

Green.

Because we negated the distance, `heappop` removes the point with the *most negative* key, which is
the *farthest* original point. So the overflow check evicts exactly the worst candidate each time,
and after the loop the heap holds the `k` nearest. We don't sort the result because the problem
doesn't ask us to, and not sorting keeps it at O(n log k).

### Refactor

This is the same bounded heap as Problem 1, with two adjustments: a max-heap instead of a min-heap
(the negation), and a computed key (`-distance`) instead of the value itself. Pulling those two
changes into focus is the whole lesson of the chapter. If you've internalised "negate for max" and
"heap on a computed key", you can adapt this skeleton to most top-`k` questions an interviewer
throws at you. No code to move; re-run the tests one last time.

## Wrapping up

- **A heap keeps the extreme reachable in O(log n)** so you can answer "smallest", "largest", or
  "top `k`" without sorting the whole input. `heapify` is the O(n) way to start one.
- **There's no max-heap in the standard library.** Negate on the way in and negate on the way out: a
  min-heap of `-x` is a max-heap of `x`. Memorise this one.
- **A bounded heap of size `k` is the top-`k` workhorse.** Push everything, pop whenever you exceed
  `k`, and the survivors are your answer in O(n log k).
- **Heap on a computed key, not the raw value.** Tuple it as `(key, payload)` (frequency, or squared
  distance) and let tuple comparison do the ordering.

Next: [Intervals](intervals.md), where a heap of end-times tells you when a meeting room frees up.
