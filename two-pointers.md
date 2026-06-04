# Two Pointers

**[You can find all the code for this chapter here](two_pointers/)**

This is the first **interview pattern** chapter, so a word on how these work. Each pattern
chapter has:

1. **When to reach for it** — the signals in a problem that say "use this pattern".
2. **The template** — a reusable skeleton in [`two_pointers/_template.py`](two_pointers/_template.py),
   the pattern in the abstract.
3. **Worked problems** — real problems in `two_pointers/solutions/`, each built test-first.

## When to reach for two pointers

Two pointers replace a nested loop (O(n²)) with a single pass (O(n)) by maintaining two indices
and an **invariant** between them. Reach for it when:

- The array is **sorted** (or can be), and you're looking for a pair/triple with some sum or
  relationship → **opposite direction** (pointers start at the ends, move inward).
- You're **filtering or partitioning in place**, or detecting a cycle → **same direction**
  (a slow "write/boundary" pointer and a fast "scan" pointer).

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

The invariant is the whole game. For opposite-direction two-sum it's "the answer, if any, lies
between `left` and `right`". For same-direction filtering it's "`arr[:slow]` holds the kept
elements so far".

## Problem 1: Valid Palindrome (opposite direction)

> Return whether a string is a palindrome, considering only alphanumeric characters and
> ignoring case.

### Write the test first

```python
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("A man, a plan, a canal: Panama", True),
        ("race a car", False),
        ("", True),
        ("0P", False),
    ],
)
def test_is_palindrome(text, expected):
    assert is_palindrome(text) is expected
```

The empty string and `"0P"` (a digit vs a letter) are the edge cases that catch naive
solutions.

### Make it pass

Pointers at both ends; skip non-alphanumeric characters; compare case-insensitively; walk
inward.

```python
def is_palindrome(s):
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

The inner `while` loops are why this is O(n): each pointer only ever moves inward, so across the
whole run we do at most `n` moves.

## Problem 2: Two Sum II — sorted input (opposite direction)

> Given a **sorted** array and a target, return the indices of the two numbers that sum to it.

### Write the test first

```python
def test_finds_the_pair():
    assert two_sum([2, 7, 11, 15], 9) == (0, 1)


def test_walks_inward_past_the_ends():
    assert two_sum([-3, 0, 1, 4, 10], 5) == (2, 3)


def test_no_solution_returns_none():
    assert two_sum([1, 2, 3], 100) is None
```

### Make it pass

Because it's sorted, the sum of the ends tells you which way to move: too small → raise the
floor (`left += 1`); too big → lower the ceiling (`right -= 1`).

```python
def two_sum(numbers, target):
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

No hash map, O(1) extra space — the payoff for the array being sorted.

## Problem 3: Remove Duplicates from Sorted Array (same direction)

> Remove duplicates from a sorted list **in place**; return the new length `k`, with the first
> `k` elements holding the unique values.

### Write the test first

```python
def test_removes_duplicates_in_place():
    nums = [1, 1, 2, 2, 3]
    k = remove_duplicates(nums)
    assert k == 3
    assert nums[:k] == [1, 2, 3]


def test_all_same():
    nums = [7, 7, 7, 7]
    assert remove_duplicates(nums) == 1
```

### Make it pass

`slow` marks the last unique slot; `fast` scans. When `fast` finds something new, advance
`slow` and write it there.

```python
def remove_duplicates(nums):
    if not nums:
        return 0
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1
```

This is the same-direction template specialised: the slow pointer is the write head, the fast
pointer reads ahead.

## Wrapping up

- **Two pointers turn O(n²) into O(n)** by maintaining an invariant between two indices.
- **Opposite direction** for sorted/symmetric pair problems (palindrome, two-sum, container).
- **Same direction (fast/slow)** for in-place filtering and cycle detection.
- The invariant is the design — state it before you code, and the pointer moves follow.

Next: [Sliding Window](sliding-window.md), two pointers' close cousin.
