# Two Pointers

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/two_pointers)**

This is the first **interview pattern** chapter, so a word on how these work. Each pattern
chapter has three parts: a "when to reach for it" section that names the signals in a problem,
a reusable template in `two_pointers/_template.py` that shows the
pattern in the abstract, and a handful of real problems in `two_pointers/solutions/`, each built
test-first.

## When to reach for two pointers

Two pointers replace a nested loop (O(n²)) with a single pass (O(n)) by keeping two indices and
an **invariant** between them. Two shapes cover most problems:

- The array is **sorted** (or can be), and you're looking for a pair or triple with some sum or
  relationship. Reach for **opposite direction**: the pointers start at the ends and move inward.
- You're **filtering or partitioning in place**, or detecting a cycle. Reach for **same
  direction**: a slow "write/boundary" pointer and a fast "scan" pointer, both starting at the
  left.

The invariant is the whole game. For opposite-direction two-sum it's "the answer, if any, lies
between `left` and `right`". For same-direction filtering it's "`arr[:slow]` holds the kept
elements so far". State the invariant before you write the loop and the pointer moves follow.

## The template

```python
def two_pointers_opposite(arr, should_move_left):
    left, right = 0, len(arr) - 1
    while left < right:
        if should_move_left(arr[left], arr[right]):
            left += 1
        else:
            right -= 1
    return left, right


def two_pointers_same(arr, keep):
    slow = 0
    for fast in range(len(arr)):
        if keep(arr[fast]):
            arr[slow] = arr[fast]
            slow += 1
    return slow
```

Both are directional skeletons. `should_move_left` and `keep` are the hooks each problem fills
in. The opposite-direction version returns the final indices; most problems read off an answer as
they walk. The same-direction version returns the new logical length, with `arr[:length]` holding
the kept elements.

## Problem 1: Valid Palindrome (opposite direction)

> Return whether a string is a palindrome, considering only alphanumeric characters and
> ignoring case.

The "compare from both ends inward" shape is the signal: a palindrome is symmetric, so opposite
pointers that meet in the middle check every pair exactly once.

### Write the test first

```python
import pytest

from valid_palindrome import is_palindrome


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("A man, a plan, a canal: Panama", True),
        ("race a car", False),
        ("", True),  # empty string is a palindrome
        (" ", True),  # only non-alphanumeric -> vacuously a palindrome
        ("a", True),  # single character
        ("ab", False),
        ("0P", False),  # digit vs letter, not equal even after lowercasing
        ("Madam", True),
    ],
)
def test_is_palindrome(text, expected):
    assert is_palindrome(text) is expected
```

The empty string, the all-spaces string, and `"0P"` (a digit versus a letter) are the edge cases
that catch naive solutions.

### Try to run the test

We've imported `is_palindrome` from a module that doesn't define it yet, so the import is the
first thing to break:

```
ImportError: cannot import name 'is_palindrome' from 'valid_palindrome'
```

Listen to the error: it's telling us where to start.

### Write the minimal amount of code for the test to run and check the failing test output

Give it an `is_palindrome` that ignores its argument and returns a stub `True`. We're not solving
anything yet. We just want the test to run so we can watch it fail on a value, which proves the
test checks what we think it does.

```python
from __future__ import annotations


def is_palindrome(s: str) -> bool:
    return True
```

Run `uv run pytest`:

```
    def test_is_palindrome(text, expected):
>       assert is_palindrome(text) is expected
E       assert True is False
E        +  where True = is_palindrome('race a car')
```

The test runs and fails on the value, not on a missing name. The cases that expect `True` pass by
luck (our stub always returns `True`), and the ones that expect `False` fail. That's exactly what
we want before writing the real thing.

### Write enough code to make it pass

Pointers at both ends. Skip non-alphanumeric characters, compare case-insensitively, walk inward.

```python
from __future__ import annotations


def is_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True
```

Run the tests again and they're green.

### Refactor

There's little to tidy in a dozen lines, but it's worth naming why this is O(n). The inner `while`
loops look like nested loops that should multiply the cost, but each pointer only ever moves
inward, so across the whole run we do at most `n` moves total. The work is bounded by how far the
pointers travel, not by the nesting. This is exactly the opposite-direction skeleton from the
template, with the alphanumeric skip as its `should_move_left` hook. Re-run the tests to confirm
nothing moved.

## Problem 2: Two Sum II, sorted input (opposite direction)

> Given a **sorted** array and a target, return the indices of the two numbers that sum to it.

The word **sorted** is the signal. On a sorted array the sum of the two ends tells you which way
to move, so you never need a nested scan or a hash map.

### Write the test first

```python
from two_sum_sorted import two_sum


def test_finds_the_pair():
    assert two_sum([2, 7, 11, 15], 9) == (0, 1)


def test_pair_in_the_middle():
    assert two_sum([2, 3, 4], 6) == (0, 2)


def test_walks_inward_past_the_ends():
    # target 5: the ends (-3, 10) overshoot, so both pointers walk inward to 1 + 4.
    assert two_sum([-3, 0, 1, 4, 10], 5) == (2, 3)


def test_no_solution_returns_none():
    assert two_sum([1, 2, 3], 100) is None


def test_empty_returns_none():
    assert two_sum([], 0) is None
```

`test_walks_inward_past_the_ends` is the one that earns its keep: the ends overshoot, so both
pointers have to move before they land on the pair. `test_empty_returns_none` pins down what
happens when there's nothing to search.

### Try to run the test

The function doesn't exist yet, so the import is what fails first:

```
ImportError: cannot import name 'two_sum' from 'two_sum_sorted'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub `two_sum` to return `None` so the tests run. The two "no solution" cases will pass by luck
(they expect `None`), and the rest will fail on the value:

```python
from __future__ import annotations


def two_sum(numbers: list[int], target: int) -> tuple[int, int] | None:
    return None
```

Run `uv run pytest`:

```
    def test_finds_the_pair():
>       assert two_sum([2, 7, 11, 15], 9) == (0, 1)
E       assert None == (0, 1)
E        +  where None = two_sum([2, 7, 11, 15], 9)
```

It runs and fails on the value. Good, now let's make the rest pass for the right reason.

### Write enough code to make it pass

Because it's sorted, the sum of the ends tells you which way to move. Too small means raise the
floor (`left += 1`), too big means lower the ceiling (`right -= 1`).

```python
from __future__ import annotations


def two_sum(numbers: list[int], target: int) -> tuple[int, int] | None:
    left, right = 0, len(numbers) - 1
    while left < right:
        current = numbers[left] + numbers[right]
        if current == target:
            return (left, right)
        if current < target:
            left += 1
        else:
            right -= 1
    return None
```

The tests pass.

### Refactor

Nothing to rewrite, but notice the payoff: no hash map, O(1) extra space, one pass. That's the
reward for the array being sorted. The brute-force version would test every pair at O(n²) and
allocate nothing useful; here the sortedness lets a single comparison rule out a whole side of the
search each step. Re-run the tests.

## Problem 3: Remove Duplicates from Sorted Array (same direction)

> Remove duplicates from a sorted list **in place**, return the new length `k`, with the first
> `k` elements holding the unique values.

"In place" and "return the new length" are the signal for same direction. A slow write pointer
marks where the next unique value goes, a fast pointer scans ahead.

### Write the test first

```python
from remove_duplicates import remove_duplicates


def test_removes_duplicates_in_place():
    nums = [1, 1, 2, 2, 3]
    k = remove_duplicates(nums)
    assert k == 3
    assert nums[:k] == [1, 2, 3]


def test_no_duplicates_unchanged():
    nums = [1, 2, 3]
    assert remove_duplicates(nums) == 3
    assert nums == [1, 2, 3]


def test_all_same():
    nums = [7, 7, 7, 7]
    k = remove_duplicates(nums)
    assert k == 1
    assert nums[:k] == [7]


def test_empty():
    assert remove_duplicates([]) == 0


def test_single():
    nums = [5]
    assert remove_duplicates(nums) == 1
    assert nums[:1] == [5]
```

We check both halves of the contract: the returned length and the contents of `nums[:k]`.
`test_all_same` and `test_empty` are the cases that catch off-by-one mistakes in the write head.

### Try to run the test

Nothing to import yet:

```
ImportError: cannot import name 'remove_duplicates' from 'remove_duplicates'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub `remove_duplicates` to return `0` so the tests run. `test_empty` will pass by luck (it
expects `0`), and the rest fail on the value:

```python
from __future__ import annotations


def remove_duplicates(nums: list[int]) -> int:
    return 0
```

Run `uv run pytest`:

```
    def test_removes_duplicates_in_place():
        nums = [1, 1, 2, 2, 3]
        k = remove_duplicates(nums)
>       assert k == 3
E       assert 0 == 3
```

Failing on the value, as expected. The one green test (`test_empty`) passes only because the stub
happens to return what it wants, a fine reminder that one green test proves nothing on its own.

### Write enough code to make it pass

`slow` marks the last unique slot, `fast` scans. When `fast` finds something new, advance `slow`
and write it there.

```python
from __future__ import annotations


def remove_duplicates(nums: list[int]) -> int:
    if not nums:
        return 0
    slow = 0  # nums[:slow + 1] are the uniques found so far
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1
```

The tests pass.

### Refactor

This is the same-direction template specialised: the slow pointer is the write head, the fast
pointer reads ahead. The one wrinkle versus `two_pointers_same` is that we compare each element
against the last kept one (`nums[slow]`) rather than against a fixed `keep` predicate, because
"is this a duplicate" depends on what we've already written. The list being sorted is what makes
that local comparison enough: equal values sit next to each other, so we never have to look back
further than `slow`. Re-run the tests to confirm.

## Wrapping up

- **Two pointers turn O(n²) into O(n)** by keeping an invariant between two indices.
- **Opposite direction** for sorted or symmetric pair problems (palindrome, two-sum, container).
- **Same direction (fast/slow)** for in-place filtering and cycle detection.
- The invariant is the design: state it before you code, and the pointer moves follow.
