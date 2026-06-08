# Stack and Monotonic Stack

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/stack_and_monotonic_stack)**

A stack is a list you only touch at one end: push on the right, pop from the right, last in first
out. The *monotonic stack* is the same list with one rule added, and that rule turns a class of
"look ahead until you find a bigger one" problems from O(n²) into a single pass.

## When to reach for a stack

A plain stack is the right tool when you're matching things that nest: brackets, tags, function
calls. You push when you open something and pop when you close it, and the most recent thing you
opened is the one sitting on top, ready to be checked.

Reach for a *monotonic* stack when the question is about the **next (or previous) greater or
smaller element**. The signals:

- You're scanning an array and, for each item, you want the first later item that beats it (next
  warmer day, next greater price, next taller building).
- A brute-force solution would, for each index, walk forward until it finds the answer. That's the
  O(n²) double loop a monotonic stack collapses.

The whole trick: keep the stack sorted (here, decreasing). When a new value breaks that order, the
elements you pop to restore it have just found their answer. It's the new value.

## The template

Here's the skeleton from `stack_and_monotonic_stack/_template.py`.
It solves the bare "next greater element": for each index, the value of the next strictly-greater
element to its right, or `-1` if there isn't one.

```python
from __future__ import annotations

from collections.abc import Sequence


def next_greater(nums: Sequence[int]) -> list[int]:
    result = [-1] * len(nums)
    stack: list[int] = []  # holds indices whose answer is not yet known
    for i, value in enumerate(nums):
        while stack and nums[stack[-1]] < value:
            result[stack.pop()] = value
        stack.append(i)
    return result
```

The stack holds **indices, not values**. That's deliberate: an index lets us look up the value
with `nums[i]` *and* write the answer into `result[i]` when we find it. If we stored values we'd
lose track of where to put the answer.

The invariant is the part to memorise: **the values at the indices on the stack are strictly
decreasing from bottom to top**. Every index goes on the stack still waiting for its answer. When
`value` is bigger than the value under the top index, that top index has found its next-greater, so
we pop it and record `value`. We keep popping while the order is broken, then push the current index
to wait its turn.

Each index is pushed once and popped at most once, so the `while` loop across the whole run does at
most `n` pops total. The scan is O(n), not the O(n²) you'd get from a forward walk per index.

Three problems, three shapes of the same idea. The first uses a plain stack; the other two are
monotonic.

## Problem 1: Valid Parentheses

> Given a string of brackets `()`, `[]`, and `{}`, return `True` if every bracket is closed by the
> matching type in the right order.

This is the nesting case, so a plain stack with no ordering rule. Push every opener; when a closer
arrives, the opener it must match is whatever's on top.

### Write the test first

```python
from valid_parentheses import is_valid


def test_single_pair():
    assert is_valid("()") is True


def test_mixed_pairs():
    assert is_valid("()[]{}") is True


def test_nested():
    assert is_valid("([{}])") is True


def test_wrong_order():
    assert is_valid("(]") is False


def test_interleaved_is_invalid():
    assert is_valid("([)]") is False


def test_unclosed_opener():
    assert is_valid("(") is False


def test_stray_closer():
    assert is_valid(")") is False


def test_empty_is_valid():
    assert is_valid("") is True
```

`test_interleaved_is_invalid` is the case that earns its keep. `([)]` has equal numbers of every
bracket, so a naive counter passes it, but the nesting is wrong: you can't close `(` while `[` is
still open. Only a stack catches that.

### Try to run the test

Nothing defines `is_valid` yet, so the import is the first thing to break:

```
ModuleNotFoundError: No module named 'stack_and_monotonic_stack.solutions.valid_parentheses'
```

The error is telling us where to start: there's no module to import from.

### Write the minimal amount of code for the test to run and check the failing test output

Give it an `is_valid` that always returns `False`. We're not solving anything, we just want the test
to run so we can watch it fail on the value and prove the test checks what we think.

```python
from __future__ import annotations


def is_valid(s: str) -> bool:
    return False
```

Run `uv run pytest`:

```
    def test_single_pair():
>       assert is_valid("()") is True
E       AssertionError: assert False is True
```

The test runs and fails on the value, not on a missing name. The cases expecting `False` (like
`test_stray_closer`) pass by luck, because `False` is exactly what the stub returns. That's a fine
reminder that a green test proves nothing on its own.

### Write enough code to make it pass

Walk the string. When we hit an opener, push it. When we hit a closer, the top of the stack has to
be its matching opener, or the string is invalid. At the end the stack has to be empty, otherwise
something was opened and never closed.

```python
from __future__ import annotations


def is_valid(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for char in s:
        if char in pairs:
            if not stack or stack.pop() != pairs[char]:
                return False
        else:
            stack.append(char)
    return not stack
```

The tests pass.

The `pairs` dict maps each closer to the opener it needs, so `char in pairs` is how we tell a closer
from an opener. Two ways to fail fast: `not stack` means a closer arrived with nothing open
(`test_stray_closer`), and `stack.pop() != pairs[char]` means the most recent opener is the wrong
type (`test_wrong_order`). The final `return not stack` handles the leftover opener in
`test_unclosed_opener`, and it makes the empty string `True` for free, since an empty stack is what
we want there anyway.

### Refactor

There's little to tidy in ten lines. The one thing worth naming is that we never needed the
monotonic rule here: the stack's job is purely "what did I most recently open", and last-in-first-out
is the whole answer. **A plain stack handles nesting; the ordering rule is what we add next.**

## Problem 2: Daily Temperatures

> Given a list of daily temperatures, return a list where each entry is how many days you'd wait
> until a strictly warmer day, or `0` if no warmer day comes.

This is next-greater-element wearing a hat. The answer isn't the warmer temperature itself, it's the
*distance* to it, which is exactly why the stack holds indices: we subtract them.

### Write the test first

```python
from daily_temperatures import daily_temperatures


def test_typical_run():
    assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]


def test_strictly_increasing():
    assert daily_temperatures([30, 40, 50, 60]) == [1, 1, 1, 0]


def test_strictly_decreasing():
    assert daily_temperatures([60, 50, 40, 30]) == [0, 0, 0, 0]


def test_equal_temperatures_never_count():
    assert daily_temperatures([50, 50, 50]) == [0, 0, 0]


def test_single_day():
    assert daily_temperatures([42]) == [0]


def test_empty():
    assert daily_temperatures([]) == []
```

`test_equal_temperatures_never_count` pins down the word *strictly*. A day that's the same
temperature doesn't count as warmer, so `[50, 50, 50]` is all zeros. Get the comparison wrong (`<=`
where you meant `<`) and this test fails while the others might not.

### Try to run the test

No module yet, so the import fails first:

```
ModuleNotFoundError: No module named 'stack_and_monotonic_stack.solutions.daily_temperatures'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return all zeros so the test runs:

```python
from __future__ import annotations

from collections.abc import Sequence


def daily_temperatures(temps: Sequence[int]) -> list[int]:
    return [0] * len(temps)
```

Run `uv run pytest`:

```
    def test_typical_run():
>       assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
E       assert [0, 0, 0, 0, 0, 0, ...] == [1, 1, 4, 2, 1, 1, ...]
E         At index 0 diff: 0 != 1
```

Failing on the values, as we wanted. The all-zeros stub passes the decreasing, equal, single, and
empty cases by luck, because their answers happen to be zeros. The two cases with a real wait
distance fail, which is the whole point of the problem.

### Write enough code to make it pass

Same shape as the template. The stack holds indices of days still waiting for a warmer one, kept so
their temperatures decrease down the stack. When today is warmer than the day under the top index,
that day's wait is over, and the wait length is the gap between the two indices.

```python
from __future__ import annotations

from collections.abc import Sequence


def daily_temperatures(temps: Sequence[int]) -> list[int]:
    result = [0] * len(temps)
    stack: list[int] = []  # indices of days still waiting for a warmer day
    for i, temp in enumerate(temps):
        while stack and temps[stack[-1]] < temp:
            j = stack.pop()
            result[j] = i - j
        stack.append(i)
    return result
```

Green.

Two changes from the template, both because the question asks for distance, not value. We seed
`result` with `0` instead of `-1`, since "no warmer day" is reported as `0` here. And we write
`i - j` (the gap between the warmer day and the waiting day) instead of the temperature. The strict
`<` is what makes equal temperatures not count: a day equal to the top stays on the stack rather than
being popped.

### Refactor

Nothing to tidy in the algorithm. It's worth seeing how little we changed from the template though:
the loop, the `while`, the push are identical, and only the two lines that *record the answer* moved.
**That's the monotonic stack as a reusable shape: keep the scan, swap what you write when an index
pops.** Re-run the tests to confirm.

## Problem 3: Next Greater Element II

> Same as next-greater-element, but the array is circular: after the last element you wrap back
> around to the first. Return the next strictly-greater value for each index, or `-1` if none exists
> anywhere on the ring.

The wrap is the twist. In `[1, 2, 1]` the last `1` has nothing greater to its right, but going
around the ring it sees the `2`, so its answer is `2`, not `-1`. We need each element to be able to
look past the end of the array and back to the start.

### Write the test first

```python
from next_greater_element_ii import next_greater_circular


def test_wraps_around():
    assert next_greater_circular([1, 2, 1]) == [2, -1, 2]


def test_all_equal_have_no_greater():
    assert next_greater_circular([5, 5, 5]) == [-1, -1, -1]


def test_descending_wraps_to_the_max():
    assert next_greater_circular([5, 4, 3, 2, 1]) == [-1, 5, 5, 5, 5]


def test_ascending():
    assert next_greater_circular([1, 2, 3, 4]) == [2, 3, 4, -1]


def test_single_element():
    assert next_greater_circular([7]) == [-1]


def test_duplicates_take_next_strictly_greater():
    assert next_greater_circular([1, 2, 3, 2, 1]) == [2, 3, -1, 3, 2]
```

`test_descending_wraps_to_the_max` is the case that forces the wrap to actually work. Every element
except the first finds the leading `5` only by going around the end. Without the circular pass they'd
all be `-1`.

### Try to run the test

No module yet:

```
ModuleNotFoundError: No module named 'stack_and_monotonic_stack.solutions.next_greater_element_ii'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return all `-1`, the "no answer" filler:

```python
from __future__ import annotations

from collections.abc import Sequence


def next_greater_circular(nums: Sequence[int]) -> list[int]:
    return [-1] * len(nums)
```

Run `uv run pytest`:

```
    def test_wraps_around():
>       assert next_greater_circular([1, 2, 1]) == [2, -1, 2]
E       assert [-1, -1, -1] == [2, -1, 2]
E         At index 0 diff: -1 != 2
```

Failing on the values. The all-equal and single-element cases pass by luck (their answers really are
all `-1`), and everything with a real next-greater fails.

### Write enough code to make it pass

The neat trick for a circular array: **iterate `2n` times and index with `step % n`**. The first
`n` steps push indices as usual; the second `n` steps push nothing but still let earlier indices find
a greater value that lives past the wrap. After two laps every index has seen the whole ring.

```python
from __future__ import annotations

from collections.abc import Sequence


def next_greater_circular(nums: Sequence[int]) -> list[int]:
    n = len(nums)
    result = [-1] * n
    stack: list[int] = []  # indices whose answer is not yet known
    for step in range(2 * n):
        value = nums[step % n]
        while stack and nums[stack[-1]] < value:
            result[stack.pop()] = value
        if step < n:
            stack.append(step)
    return result
```

The tests pass.

`step % n` is what folds the second lap back onto the same array. The `if step < n` guard is the one
line that keeps it correct: we only *push* during the first lap, so no index is added twice, but we
still *pop* during the second lap, which is how the wrap resolves answers. Anything left on the stack
after `2n` steps genuinely has no greater element anywhere, and it keeps its seeded `-1`.

### Refactor

No tidy needed, but notice the cost. We do `2n` iterations instead of `n`, yet each index is still
pushed once and popped at most once, so the work is `2 * O(n)`, which is still O(n). **Doubling the
loop count to fake a ring doesn't change the complexity class.** Re-run the tests and we're done.

## Wrapping up

- **A plain stack matches nested structure**: push openers, pop to check closers, the most recent
  open thing is always on top. That solved valid parentheses with no ordering rule.
- **A monotonic stack keeps its values sorted, and the pop is the answer.** When a new value breaks
  the order, every index you pop has just found its next-greater (or next-warmer) element.
- **Store indices, not values.** An index lets you read `nums[i]` and write `result[i]`, which is how
  daily temperatures reports a distance instead of a value.
- **The invariant is the whole pattern**: strictly decreasing values on the stack, each index pushed
  once and popped once, so the scan is O(n) where the brute force is O(n²).
- **For a circular array, iterate `2n` and index with `% n`, pushing only on the first lap.** The
  complexity stays O(n).
