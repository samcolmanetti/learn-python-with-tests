# Sliding Window

**[You can find all the code for this chapter here](sliding_window/)**

A sliding window is two pointers with a job: maintain a contiguous range `[left, right]` and
slide it across the input, adding the element that enters and removing the one that leaves. Each
element is added and removed once, so the whole scan is O(n).

## When to reach for it

The tell is a question about a **contiguous subarray or substring** — "longest", "shortest",
"maximum sum of size k", "smallest window containing…". Three shapes cover almost everything:

| Shape | You're asked for… | Move pattern |
|-------|-------------------|--------------|
| **Fixed** | best window of exactly size `k` | slide a constant-width window |
| **Flexible — longest** | the *longest* window that stays valid | grow right; shrink left only when invalid |
| **Flexible — shortest** | the *shortest* window that's valid | grow right; shrink left while still valid |

The template ([`sliding_window/_template.py`](sliding_window/_template.py)) has one function per
shape. Below we ground each in a real problem.

## Problem 1: Maximum Sum Subarray of Size K (fixed)

### Write the test first

```python
def test_basic_window():
    assert max_subarray_sum([1, 4, 2, 10, 2, 3], 3) == 16  # [4, 2, 10]


def test_handles_negatives():
    assert max_subarray_sum([-1, -2, -3, -4], 2) == -3


@pytest.mark.parametrize("bad_k", [0, -1, 5])
def test_invalid_window_size_raises(bad_k):
    with pytest.raises(ValueError):
        max_subarray_sum([1, 2, 3], bad_k)
```

### Make it pass

Compute the first window's sum once, then each slide is a single add-and-subtract — O(1) per
step instead of re-summing `k` elements.

```python
def max_subarray_sum(nums, k):
    if k <= 0 or k > len(nums):
        raise ValueError(f"window size {k} invalid for input of length {len(nums)}")
    window = sum(nums[:k])
    best = window
    for right in range(k, len(nums)):
        window += nums[right] - nums[right - k]  # add entering, drop leaving
        best = max(best, window)
    return best
```

## Problem 2: Longest Substring Without Repeating Characters (flexible — longest)

### Write the test first

```python
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("abcabcbb", 3),  # "abc"
        ("bbbbb", 1),
        ("pwwkew", 3),    # "wke"
        ("", 0),
        ("abba", 2),      # left must not move backwards
    ],
)
def test_length_of_longest_substring(text, expected):
    assert length_of_longest_substring(text) == expected
```

`"abba"` is the case that breaks naive solutions: when you reach the second `a`, `left` must
jump forward — but never *backwards* past where it already is.

### Make it pass

Remember each character's last index. When the entering character is already in the current
window, jump `left` to just past its previous position.

```python
def length_of_longest_substring(s):
    last_seen = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best
```

The `last_seen[ch] >= left` guard is what protects against `left` moving backwards.

## Problem 3: Find All Anagrams in a String (fixed window of counts)

### Write the test first

```python
def test_finds_two_anagrams():
    assert find_anagrams("cbaebabacd", "abc") == [0, 6]


def test_overlapping_anagrams():
    assert find_anagrams("abab", "ab") == [0, 1, 2]


def test_pattern_longer_than_string():
    assert find_anagrams("a", "aa") == []
```

### Make it pass

An anagram is a permutation, so two substrings are anagrams iff their **character counts**
match. Slide a fixed window of size `len(p)` and compare `Counter`s, updating counts
incrementally.

```python
from collections import Counter


def find_anagrams(s, p):
    if len(p) > len(s):
        return []
    need = Counter(p)
    window = Counter(s[:len(p)])
    result = [0] if window == need else []
    for right in range(len(p), len(s)):
        window[s[right]] += 1
        left_char = s[right - len(p)]
        window[left_char] -= 1
        if window[left_char] == 0:
            del window[left_char]   # drop zero entries so Counter equality works
        if window == need:
            result.append(right - len(p) + 1)
    return result
```

Deleting zero-count keys matters: `Counter({"a": 1, "b": 0}) != Counter({"a": 1})`, so leaving
stale zeros would break the comparison.

## Wrapping up

- A sliding window is **O(n)**: each element enters and leaves the window once.
- Identify the shape first — **fixed**, **longest-flexible**, or **shortest-flexible** — then
  the loop writes itself.
- **Fixed** windows update with a single add/subtract; never re-sum.
- For substring-count problems, a **`Counter` window** compared against the target is the
  go-to; remember to drop zero entries.

Next: [Binary Search](binary-search.md).
