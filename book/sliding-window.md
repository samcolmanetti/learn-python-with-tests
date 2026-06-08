# Sliding Window

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/sliding_window)**

A sliding window is two pointers with a job: maintain a contiguous range `[left, right]` and
slide it across the input, adding the element that enters and removing the one that leaves. Each
element is added and removed once, so the whole scan is O(n).

## When to reach for sliding window

The tell is a question about a **contiguous subarray or substring**: "longest", "shortest",
"maximum sum of size k", "smallest window containing...". Three shapes cover almost everything.

| Shape | You're asked for... | Move pattern |
|-------|-------------------|--------------|
| **Fixed** | best window of exactly size `k` | slide a constant-width window |
| **Flexible, longest** | the *longest* window that stays valid | grow right, shrink left only when invalid |
| **Flexible, shortest** | the *shortest* window that's valid | grow right, shrink left while still valid |

The template (`sliding_window/_template.py`) has one function per
shape. Below we ground each in a real problem.

## Problem 1: Maximum Sum Subarray of Size K (fixed)

> Given an array and a window size `k`, return the largest sum of any contiguous window of
> exactly `k` elements. An invalid `k` should raise.

This is the fixed shape. The window is always `k` wide, so the only question is how to slide it
without re-summing `k` elements every step.

### Write the test first

```python
import pytest

from subarray_sum_fixed import max_subarray_sum


def test_basic_window():
    assert max_subarray_sum([1, 4, 2, 10, 2, 3], 3) == 16  # [4, 2, 10]


def test_handles_negatives():
    assert max_subarray_sum([-1, -2, -3, -4], 2) == -3  # [-1, -2]


@pytest.mark.parametrize("bad_k", [0, -1, 5])
def test_invalid_window_size_raises(bad_k):
    with pytest.raises(ValueError):
        max_subarray_sum([1, 2, 3], bad_k)
```

`test_handles_negatives` keeps us honest: the answer is the *least negative* window, not the one
with the biggest absolute value. `test_invalid_window_size_raises` pins down what happens when
`k` is zero, negative, or wider than the array.

### Try to run the test

We're importing `max_subarray_sum` from a module that doesn't define it yet, so the import is the
first thing to break:

```
ImportError: cannot import name 'max_subarray_sum' from 'subarray_sum_fixed'
```

No function, nothing to call. Listen to the error: it tells us where to start.

### Write the minimal amount of code for the test to run and check the failing test output

Give it a `max_subarray_sum` that returns a stub `0`. We're not solving anything yet. We just
want the test to run so we can watch it fail on the value, which proves the test checks what we
think it does.

```python
from __future__ import annotations


def max_subarray_sum(nums: list[int], k: int) -> int:
    return 0
```

Run `uv run pytest`:

```
    def test_basic_window():
>       assert max_subarray_sum([1, 4, 2, 10, 2, 3], 3) == 16  # [4, 2, 10]
E       assert 0 == 16
E        +  where 0 = max_subarray_sum([1, 4, 2, 10, 2, 3], 3)
```

The test runs and fails on the value, not on a missing name. That's exactly what we want before
writing the real thing. (`test_invalid_window_size_raises` fails too, because our stub never
raises.)

### Write enough code to make it pass

Compute the first window's sum once, then each slide is a single add-and-subtract: O(1) per step
instead of re-summing `k` elements.

```python
from __future__ import annotations


def max_subarray_sum(nums: list[int], k: int) -> int:
    if k <= 0 or k > len(nums):
        raise ValueError(f"window size {k} invalid for input of length {len(nums)}")
    window = sum(nums[:k])
    best = window
    for right in range(k, len(nums)):
        window += nums[right] - nums[right - k]
        best = max(best, window)
    return best
```

The tests pass. The line `window += nums[right] - nums[right - k]` is the whole pattern: add the
element entering on the right, subtract the one leaving on the left. The window's sum stays
correct without ever looking at the middle.

### Refactor

There's little to tidy in nine lines, but it's worth naming the shape. This is the fixed-window
skeleton from the template: seed the first window, then slide with a constant-time update. The
guard at the top turns a bad `k` into a clear error instead of an out-of-range slice. Re-run the
tests to confirm nothing moved.

## Problem 2: Longest Substring Without Repeating Characters (flexible, longest)

> Return the length of the longest substring of `s` that has no repeated character.

This is the flexible-longest shape. We grow the window to the right, and when a character repeats
we shrink from the left until the window is valid (all unique) again.

### Write the test first

```python
import pytest

from longest_substring_no_repeat import length_of_longest_substring


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("abcabcbb", 3),  # "abc"
        ("bbbbb", 1),  # "b"
        ("pwwkew", 3),  # "wke"
        ("", 0),  # empty
        ("au", 2),
        ("dvdf", 3),  # "vdf", left must jump correctly
        ("abba", 2),  # left must never move backwards
    ],
)
def test_length_of_longest_substring(text, expected):
    assert length_of_longest_substring(text) == expected
```

`"abba"` is the case that breaks naive solutions. When you reach the second `a`, `left` must jump
forward, but never *backwards* past where it already is.

### Try to run the test

The function doesn't exist yet, so the import fails first:

```
ImportError: cannot import name 'length_of_longest_substring' from 'longest_substring_no_repeat'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return `0` so the tests run:

```python
from __future__ import annotations


def length_of_longest_substring(s: str) -> int:
    return 0
```

Run `uv run pytest`:

```
    def test_length_of_longest_substring(text, expected):
>       assert length_of_longest_substring(text) == expected
E       assert 0 == 3
E        +  where 0 = length_of_longest_substring('abcabcbb')
```

Failing on the value, as expected. The empty-string case (`"" == 0`) passes by luck, because our
stub returns `0`. That's a fine reminder that one green test proves nothing on its own.

### Write enough code to make it pass

Remember each character's last index. When the entering character is already in the current
window, jump `left` to just past its previous position.

```python
from __future__ import annotations


def length_of_longest_substring(s: str) -> int:
    last_seen: dict[str, int] = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best
```

The tests pass. The `last_seen[ch] >= left` guard is what protects against `left` moving
backwards: a character we saw earlier but already slid past is no longer in the window, so it
shouldn't drag `left` back.

### Refactor

The body is already tight, so the refactor here is about understanding, not lines. This is the
flexible-longest skeleton: grow `right` every step, and only move `left` when the window turns
invalid. Instead of shrinking one position at a time, the last-seen dict lets us jump `left`
straight to the fixed-up position in O(1). Re-run the tests.

## Problem 3: Find All Anagrams in a String (fixed window of counts)

> Return the start indices of every substring of `s` that is an anagram of `p`.

Back to a fixed window, but now what we track inside it is a character count, not a sum. Two
substrings are anagrams exactly when their character counts match.

### Write the test first

```python
from find_all_anagrams import find_anagrams


def test_finds_two_anagrams():
    assert find_anagrams("cbaebabacd", "abc") == [0, 6]


def test_overlapping_anagrams():
    assert find_anagrams("abab", "ab") == [0, 1, 2]


def test_no_anagrams():
    assert find_anagrams("hello", "xyz") == []


def test_pattern_longer_than_string():
    assert find_anagrams("a", "aa") == []


def test_whole_string_is_the_anagram():
    assert find_anagrams("bca", "abc") == [0]
```

`test_overlapping_anagrams` is the one that earns its keep: anagrams can overlap, so a found match
at index `0` doesn't let us skip ahead. `test_pattern_longer_than_string` covers the guard for
when `p` can't fit in `s` at all.

### Try to run the test

Nothing to import yet:

```
ImportError: cannot import name 'find_anagrams' from 'find_all_anagrams'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return an empty list so the tests run:

```python
from __future__ import annotations


def find_anagrams(s: str, p: str) -> list[int]:
    return []
```

Run `uv run pytest`:

```
    def test_finds_two_anagrams():
>       assert find_anagrams("cbaebabacd", "abc") == [0, 6]
E       assert [] == [0, 6]
E         Right contains 2 more items, first extra item: 0
```

Failing on the value. The two no-match cases (`test_no_anagrams` and
`test_pattern_longer_than_string`) pass, because they happen to expect the empty list our stub
returns. The matches all fail, which is what we want before writing the real thing.

### Write enough code to make it pass

An anagram is a permutation, so two substrings are anagrams when their **character counts** match.
Slide a fixed window of size `len(p)` and compare `Counter`s, updating the counts incrementally.

```python
from __future__ import annotations

from collections import Counter


def find_anagrams(s: str, p: str) -> list[int]:
    if len(p) > len(s):
        return []

    need = Counter(p)
    window = Counter(s[: len(p)])
    result = []

    if window == need:
        result.append(0)

    for right in range(len(p), len(s)):
        window[s[right]] += 1  # element entering on the right
        left_char = s[right - len(p)]  # element leaving on the left
        window[left_char] -= 1
        if window[left_char] == 0:
            del window[left_char]  # keep Counters comparable (no zero entries)
        if window == need:
            result.append(right - len(p) + 1)

    return result
```

The tests pass. Deleting zero-count keys matters: `Counter({"a": 1, "b": 0})` is not equal to
`Counter({"a": 1})`, so leaving stale zeros would break the comparison and we'd miss matches.

### Refactor

Nothing to tidy in the algorithm, but it's worth naming what we did. This is the same fixed-window
slide as Problem 1, with the running sum swapped for a running `Counter`. The add-on-the-right,
drop-on-the-left bookkeeping is identical in spirit: each slide touches two characters, so the
whole scan stays O(n) over a fixed alphabet. Re-run the tests.

## Wrapping up

- A sliding window is **O(n)**: each element enters and leaves the window once.
- Identify the shape first (**fixed**, **longest-flexible**, or **shortest-flexible**), then the
  loop writes itself.
- **Fixed** windows update with a single add and subtract. Never re-sum.
- For substring-count problems, a **`Counter` window** compared against the target is the go-to.
  Remember to drop zero entries so the comparison works.
