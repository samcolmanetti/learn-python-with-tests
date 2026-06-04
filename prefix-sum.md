# Prefix Sum

**[You can find all the code for this chapter here](prefix_sum/)**

Like two pointers, prefix sum is an **interview pattern**: a reusable [`prefix_sum/_template.py`](prefix_sum/_template.py)
plus worked problems in `prefix_sum/solutions/`, each built test-first. The idea is small and it
pays off everywhere: do one pass to precompute cumulative sums, then answer any range-sum query
with a single subtraction.

## When to reach for prefix sum

You're asked the sum (or count) of some range of an array, and you're asked it more than once.
The naive answer re-adds the range every time, so `q` queries over an array of length `n` cost
O(n * q). Reach for prefix sum when:

- You have **many range-sum queries** over an array that doesn't change. Precompute once, answer
  each query in O(1).
- You're counting **subarrays with a target sum**. A running prefix sum plus a hashmap of how
  often each prefix has appeared turns an O(n²) double loop into one pass.

The whole trick is that the sum of `arr[left:right]` is the difference of two cumulative sums.
If you know the total up to `right` and the total up to `left`, you subtract.

## The template

```python
def build_prefix(arr):
    prefix = [0.0] * (len(arr) + 1)
    for i, value in enumerate(arr):
        prefix[i + 1] = prefix[i] + value
    return prefix


def range_sum(prefix, left, right):
    return prefix[right + 1] - prefix[left]
```

Notice `prefix` has length `n + 1`, not `n`. We put a zero in front so that `prefix[i]` is the
sum of everything *before* index `i`, that is `prefix[i] == sum(arr[:i])`. This *leading-zero
convention* is the part worth memorising. Without it, the sum of a range starting at index `0`
becomes a special case (you'd have to write `if left == 0`). With it, `range_sum` is one clean
subtraction for every range, the first one included.

To get the inclusive sum of `arr[left:right + 1]`, we read `prefix[right + 1] - prefix[left]`.
The `right + 1` is there because our prefix is offset by that leading zero.

## Problem 1: Range Sum Query (Immutable)

> Given an integer array that never changes, answer many `sum_range(i, j)` queries, where the
> sum is inclusive of both ends. Each query should be O(1).

The phrase "never changes" and "many queries" is the signal. We pay once to build the prefix,
then every query is cheap.

### Write the test first

```python
from .range_sum_query_immutable import NumArray


def test_basic_range():
    arr = NumArray([-2, 0, 3, -5, 2, -1])
    assert arr.sum_range(0, 2) == 1


def test_full_array():
    arr = NumArray([-2, 0, 3, -5, 2, -1])
    assert arr.sum_range(0, 5) == -3


def test_single_element():
    arr = NumArray([-2, 0, 3, -5, 2, -1])
    assert arr.sum_range(3, 3) == -5


def test_repeated_queries():
    arr = NumArray([-2, 0, 3, -5, 2, -1])
    assert arr.sum_range(2, 5) == -1
    assert arr.sum_range(0, 2) == 1
    assert arr.sum_range(1, 4) == 0
```

`test_single_element` (a range where `i == j`) and `test_repeated_queries` (the same object hit
over and over) are the cases that pin down the behaviour we actually want.

### Try to run the test

We've imported `NumArray` from a module that doesn't define it yet. Let's give it a `NumArray`
that stores the array but returns a stub `0` from `sum_range`, so we can watch the test fail for
the right reason.

```python
from __future__ import annotations


class NumArray:
    def __init__(self, nums: list[int]) -> None:
        self.nums = nums

    def sum_range(self, i: int, j: int) -> int:
        return 0
```

Run `uv run pytest`:

```
    def test_basic_range():
        arr = NumArray([-2, 0, 3, -5, 2, -1])
>       assert arr.sum_range(0, 2) == 1
E       assert 0 == 1
E        +  where 0 = sum_range(0, 2)
```

The test runs and fails on the value, not on a missing name. That's exactly what we want before
writing the real thing.

### Write enough code to make it pass

Build the prefix once in `__init__` using the leading-zero convention, then `sum_range` is the
subtraction from the template. One small change from the template: we seed with `0` (an integer)
instead of `0.0`, because these sums are integers and we want `sum_range` to return an `int`. The
template used a float to stay generic over any numeric input.

```python
from __future__ import annotations


class NumArray:
    def __init__(self, nums: list[int]) -> None:
        self.prefix = [0] * (len(nums) + 1)
        for i, value in enumerate(nums):
            self.prefix[i + 1] = self.prefix[i] + value

    def sum_range(self, i: int, j: int) -> int:
        return self.prefix[j + 1] - self.prefix[i]
```

Run the tests again and they're green.

The constructor is O(n) and runs once. After that, every `sum_range` is a single subtraction,
O(1), no matter how many times it's called. That's the trade: a one-time setup cost buys
constant-time queries forever.

## Problem 2: Subarray Sum Equals K

> Count the contiguous subarrays whose elements sum to `k`.

This one looks like it wants nested loops: pick every start, every end, add up the middle. That's
O(n²). The prefix-sum reframing kills a loop, but it needs one extra idea, so let me show it.

The sum of `nums[i:j]` is `running[j] - running[i]`, where `running` is the cumulative sum. So a
subarray sums to `k` exactly when two prefix sums differ by `k`: `running[j] - running[i] == k`,
which rearranges to `running[i] == running[j] - k`. As we walk the array computing the running
sum, we ask: how many earlier prefixes equal `running - k`? A hashmap of prefix-sum frequencies
answers that in O(1).

### Write the test first

```python
from .subarray_sum_equals_k import subarray_sum


def test_repeated_ones():
    assert subarray_sum([1, 1, 1], 2) == 2


def test_distinct_values():
    assert subarray_sum([1, 2, 3], 3) == 2


def test_zero_target_with_negatives():
    assert subarray_sum([1, -1, 0], 0) == 3


def test_empty():
    assert subarray_sum([], 0) == 0


def test_single_element_hit():
    assert subarray_sum([5], 5) == 1


def test_single_element_miss():
    assert subarray_sum([5], 3) == 0
```

`test_zero_target_with_negatives` is the one that earns its keep: `[1, -1, 0]` has three
subarrays summing to zero (`[1, -1]`, `[1, -1, 0]`, and `[0]`), and you only find all three if
your counting handles negatives and a target of `0`. A solution that assumes positive numbers
quietly gets this wrong.

### Try to run the test

Stub `subarray_sum` to return `0`:

```python
from __future__ import annotations


def subarray_sum(nums: list[int], k: int) -> int:
    return 0
```

Run `uv run pytest`:

```
    def test_repeated_ones():
>       assert subarray_sum([1, 1, 1], 2) == 2
E       assert 0 == 2
E        +  where 0 = subarray_sum([1, 1, 1], 2)

FAILED test_subarray_sum_equals_k.py::test_repeated_ones
4 failed, 2 passed
```

The two that pass (`test_empty` and `test_single_element_miss`) only pass because they happen to
expect `0`, which is exactly what our stub returns. The other four fail on the value. Good, now
let's make them all pass for the right reason.

### Write enough code to make it pass

Keep a running sum and a dict mapping each prefix sum to how many times we've seen it. Seed it
with `{0: 1}`: that records the empty prefix before any elements, so a subarray that starts at
index `0` and itself sums to `k` gets counted.

```python
from __future__ import annotations

from collections import defaultdict


def subarray_sum(nums: list[int], k: int) -> int:
    counts: dict[int, int] = defaultdict(int)
    counts[0] = 1
    running = 0
    total = 0
    for value in nums:
        running += value
        total += counts[running - k]
        counts[running] += 1
    return total
```

The tests pass.

The order inside the loop matters. We add to `total` *before* recording the current prefix, so a
single element can't pair with itself as a zero-length subarray. And `{0: 1}` is the seed that
makes "the prefix up to here is exactly `k`" count as a hit, which is why `test_single_element_hit`
(`[5]` with `k=5`) returns `1` rather than `0`.

One pass, O(n) time, O(n) space for the dict. The nested loop is gone.

## Problem 3: Product of Array Except Self

> Return an array `output` where `output[i]` is the product of every element except `nums[i]`.
> No division allowed.

Why ban division? Because the obvious move (multiply everything, then divide out `nums[i]`)
explodes the moment any element is `0`. The prefix idea adapts cleanly to multiplication:
`output[i]` is the product of everything to the *left* of `i` times the product of everything to
the *right* of `i`. Two passes, no division, and zeros just take care of themselves.

### Write the test first

```python
from .product_of_array_except_self import product_except_self


def test_no_zeros():
    assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]


def test_one_zero():
    assert product_except_self([0, 4, 3]) == [12, 0, 0]


def test_two_zeros():
    assert product_except_self([0, 4, 0]) == [0, 0, 0]


def test_negatives():
    assert product_except_self([-1, 1, 2, -3]) == [-6, 6, 3, -2]
```

The zero cases are the point. With one zero, only the slot at that zero gets a non-zero product
(everything else's product includes the zero). With two zeros, every slot's product includes a
zero, so the whole result is zeros. Division can't express that without special-casing; prefix
products express it for free.

### Try to run the test

Stub it to return zeros so the test runs:

```python
from __future__ import annotations


def product_except_self(nums: list[int]) -> list[int]:
    return [0] * len(nums)
```

Run `uv run pytest`:

```
    def test_no_zeros():
>       assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
E       assert [0, 0, 0, 0] == [24, 12, 8, 6]
E         
E         At index 0 diff: 0 != 24
```

Failing on the values, as expected. (The all-zeros stub passes `test_two_zeros` by luck, which is
a fine reminder that one green test proves nothing on its own.)

### Write enough code to make it pass

First pass left to right: fill `output[i]` with the product of everything before `i`. Second pass
right to left: multiply in the product of everything after `i`. We carry the running product in a
single variable each time, so the only array we allocate is the output itself.

```python
from __future__ import annotations


def product_except_self(nums: list[int]) -> list[int]:
    n = len(nums)
    output = [1] * n

    prefix = 1
    for i in range(n):
        output[i] = prefix
        prefix *= nums[i]

    suffix = 1
    for i in range(n - 1, -1, -1):
        output[i] *= suffix
        suffix *= nums[i]

    return output
```

Green.

In the first pass, `prefix` is the product of all elements strictly before `i` when we write it,
so `output[0]` correctly gets `1` (nothing to its left). The second pass does the mirror image
with `suffix`. Multiply the two and you've got the product of everything except `nums[i]`, and
the zeros fall out naturally: a slot whose left or right product passed through a `0` becomes
`0`, no branch required.

### Refactor

There's nothing to tidy in the algorithm, but it's worth naming what we did. The first loop built
a *prefix product* and the second a *suffix product*, and we folded both into the output array
instead of allocating two more. That's the same cumulative-sum shape as the template, with `*`
swapped in for `+` and a second pass from the other end. The pattern bends.

## Wrapping up

- **Prefix sum precomputes cumulative totals once so every range query is a subtraction**, O(1)
  each, turning O(n * q) into O(n + q).
- **The leading-zero convention** (`prefix[i] == sum(arr[:i])`, length `n + 1`) removes the
  `left == 0` special case. Memorise it.
- **A running prefix plus a hashmap of prefix frequencies** counts subarrays with a target sum in
  one pass. Seed the map with `{0: 1}`.
- **The idea generalises**: swap `+` for `*` (and add a second pass) and you get prefix/suffix
  products with no division.

Next: [Stack and Monotonic Stack](stack-and-monotonic-stack.md), where the structure you carry
along the pass is a stack instead of a cumulative number.
