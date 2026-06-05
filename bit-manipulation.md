# Bit Manipulation

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/bit_manipulation)**

Underneath every integer is a string of bits, and a handful of operators let you read and edit
those bits directly. That's the whole pattern: when a problem is really about which bits are set,
the bitwise version is shorter and faster than counting, sorting, or hashing your way there.

## When to reach for bit manipulation

The signals are concrete:

- **Every element appears an even number of times except one.** XOR cancels pairs, so XORing the
  whole list leaves the odd one out. No hashmap, O(1) space.
- **You're asked to count or inspect set bits**, like the population count of a number or of a
  whole range `0..n`. Bit tricks beat converting to a string and counting characters.
- **You're tracking a small set of on/off flags**, up to 64 of them. An `int` is a free bitset:
  one bit per flag, `&` and `|` to combine, `<<` to address.

The mental model is that an `int` is an array of bits you can index and toggle without ever
allocating an array.

## The template

There's no single skeleton for bit problems the way there is for two pointers, but three operations
carry almost all of them. Here they are as tested functions in
[`bit_manipulation/_template.py`](bit_manipulation/_template.py):

```python
from __future__ import annotations


def lowest_set_bit(x: int) -> int:
    """Return the value of the lowest set bit of ``x`` (0 when ``x`` is 0)."""
    return x & -x


def clear_lowest_set_bit(x: int) -> int:
    """Return ``x`` with its lowest set bit cleared."""
    return x & (x - 1)


def is_bit_set(x: int, i: int) -> bool:
    """Return True when bit ``i`` of ``x`` is set."""
    return (x & (1 << i)) != 0
```

Three moves, and it's worth saying what each one buys you.

**XOR (`^`) cancels.** `a ^ a == 0` and `a ^ 0 == a`. XOR is its own inverse, so XORing a value in
twice undoes it. That's the trick behind finding a lone unpaired element: pair everything off and
it vanishes.

**A mask isolates a bit.** `1 << i` is a single `1` sitting at position `i`, so `x & (1 << i)`
keeps that one bit of `x` and zeroes the rest. Non-zero means the bit was set. Shift the mask
across the positions and you can walk a number bit by bit.

**`x & -x` grabs the rightmost set bit, and `x & (x - 1)` clears it.** In two's complement, `-x`
is the bitwise-not of `x` plus one, which lines up so that `x & -x` keeps only the lowest `1`.
Subtracting one flips that lowest `1` to `0` (and the zeros below it to ones), so `x & (x - 1)`
erases it. Looping on `x & (x - 1)` touches one set bit per iteration instead of all 32 or 64
positions, which matters when a number is mostly zeros.

Memorise those three. Every problem below is one of them in disguise.

## Problem 1: Single Number

> Every element in a list appears exactly twice except for one, which appears once. Return that
> one. Use O(1) extra space.

The O(1) space requirement rules out the obvious hashmap of counts. XOR is the way in: pairs
cancel, the loner survives.

### Write the test first

```python
from .single_number import single_number


def test_single_in_the_middle():
    assert single_number([2, 2, 1]) == 1


def test_single_with_repeats_spread_out():
    assert single_number([4, 1, 2, 1, 2]) == 4


def test_only_one_element():
    assert single_number([7]) == 7


def test_zero_is_a_valid_answer():
    assert single_number([3, 0, 3]) == 0


def test_handles_negatives():
    assert single_number([-5, 9, 9]) == -5
```

`test_zero_is_a_valid_answer` pins down a corner that a careless implementation gets wrong: the
answer can be `0`, so you can't use `0` as a "not found" sentinel. And `test_handles_negatives`
checks that the trick survives negative inputs, which it does, because Python's integers XOR fine
across signs.

### Try to run the test

The module doesn't define the function yet, so the import is what breaks first:

```
ImportError: cannot import name 'single_number' from 'bit_manipulation.solutions.single_number'
```

Listen to the error. It's pointing us at the one name we owe it.

### Write the minimal amount of code for the test to run and check the failing test output

Give it a `single_number` that returns a stub `0`. We're not solving anything yet, we just want
the test to run and fail on the value so we know it's checking what we think.

```python
from __future__ import annotations

from collections.abc import Iterable


def single_number(nums: Iterable[int]) -> int:
    return 0
```

Run `uv run pytest`:

```
    def test_single_in_the_middle():
>       assert single_number([2, 2, 1]) == 1
E       assert 0 == 1
E        +  where 0 = single_number([2, 2, 1])
```

Four tests fail on the value, and `test_zero_is_a_valid_answer` passes, but only by accident: its
expected answer happens to be the `0` our stub always returns. That one freebie is a good reminder
that a single green test proves nothing on its own.

### Write enough code to make it pass

XOR everything together, starting from `0`. Pairs cancel to `0`, and `0 ^ x` is `x`, so what's
left at the end is the single element.

```python
from __future__ import annotations

from collections.abc import Iterable
from functools import reduce
from operator import xor


def single_number(nums: Iterable[int]) -> int:
    return reduce(xor, nums, 0)
```

`reduce(xor, nums, 0)` folds `^` across the list with an initial accumulator of `0`. The `0` seed
is also what makes `test_only_one_element` work: a one-element list reduces to `0 ^ 7 == 7`.

The tests pass.

### Refactor

`reduce(xor, nums, 0)` is already a single expression, so there's nothing to shrink. The thing to
appreciate is the cost. We make one pass, O(n) time, and carry a single integer, O(1) space, which
is exactly what the problem asked for and what a counting dict could never give us. If you find a
plain loop clearer, `result = 0; for x in nums: result ^= x; return result` is the same algorithm
spelled out, and I'd happily write either in an interview.

## Problem 2: Number of 1 Bits

> Given a non-negative integer, return how many bits are set to `1` in it. (This is the *Hamming
> weight*, or *population count*.)

You could turn the number into a binary string and count the ones, and honestly that's a fine
interview answer. But the bit trick is tighter and it shows off `x & (x - 1)` from the template, so
let's build that one.

### Write the test first

```python
from .number_of_1_bits import hamming_weight


def test_zero_has_no_set_bits():
    assert hamming_weight(0) == 0


def test_one_set_bit():
    assert hamming_weight(8) == 1


def test_all_set_bits():
    assert hamming_weight(0b1111) == 4


def test_mixed_bits():
    assert hamming_weight(0b1011) == 3


def test_large_value():
    assert hamming_weight(0xFFFFFFFF) == 32
```

The `0b1111` and `0xFFFFFFFF` literals say exactly which bits we mean, which makes the expected
counts obvious to a reader: four ones, then a full 32-bit word of ones. `test_zero_has_no_set_bits`
is the base case the loop has to terminate on.

### Try to run the test

No function yet, so the import fails:

```
ImportError: cannot import name 'hamming_weight' from 'bit_manipulation.solutions.number_of_1_bits'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return `0` so the suite runs:

```python
from __future__ import annotations


def hamming_weight(n: int) -> int:
    return 0
```

Run `uv run pytest`:

```
    def test_one_set_bit():
>       assert hamming_weight(8) == 1
E       assert 0 == 1
E        +  where 0 = hamming_weight(8)
```

Failing on the value, and again `test_zero_has_no_set_bits` rides along green because zero really
does have zero set bits. Now let's make the rest pass for the right reason.

### Write enough code to make it pass

Loop while `n` is non-zero. Each step, clear the lowest set bit with `n & (n - 1)` and add one to
the count. The loop runs exactly once per set bit and then stops.

```python
from __future__ import annotations


def hamming_weight(n: int) -> int:
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count
```

Green.

Why `n & (n - 1)` instead of checking all 32 positions? Because it skips the zeros. Subtracting one
from `n` flips the rightmost `1` to `0` and turns every `0` below it into a `1`; ANDing that back
with `n` wipes out the rightmost `1` and leaves everything above it untouched. So each iteration
removes exactly one set bit, and a number with three set bits loops three times, no matter how far
apart those bits sit. **The loop cost is the number of set bits, not the width of the integer.**

### Refactor

The body is four lines and every one earns its place, so there's no tidying to do here. It's worth
noting the standard library has `int.bit_count()` (Python 3.10+) and the older `bin(n).count("1")`,
either of which you'd reach for in real code. We wrote the loop because the point of the chapter is
the `x & (x - 1)` move, and that move turns up again in problems where you actually need to *visit*
each set bit, not just tally them.

## Problem 3: Counting Bits

> Given an integer `n`, return a list of length `n + 1` where entry `i` is the number of set bits
> in `i`, for every `i` from `0` to `n`.

The lazy answer calls our `hamming_weight` on each `i`, which is O(n log n) overall. We can do
better with one observation: the bit count of `i` is the bit count of `i` with its last bit dropped,
plus that last bit. Each answer reuses one we already computed, so the whole thing is O(n).

### Write the test first

```python
from .counting_bits import count_bits


def test_zero():
    assert count_bits(0) == [0]


def test_up_to_two():
    assert count_bits(2) == [0, 1, 1]


def test_up_to_five():
    assert count_bits(5) == [0, 1, 1, 2, 1, 2]


def test_length_matches_n_plus_one():
    assert len(count_bits(10)) == 11


def test_matches_naive_count():
    expected = [bin(i).count("1") for i in range(16)]
    assert count_bits(15) == expected
```

`test_matches_naive_count` is the one I trust most: it builds the expected list with the obvious
`bin(i).count("1")` and asserts our clever recurrence agrees with it across all sixteen values.
When a fast solution has to match a slow-but-undeniable one, that's a property worth asserting
directly. `test_length_matches_n_plus_one` guards the off-by-one in the list size.

### Try to run the test

Nothing to import yet:

```
ImportError: cannot import name 'count_bits' from 'bit_manipulation.solutions.counting_bits'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return an empty list so the tests run:

```python
from __future__ import annotations


def count_bits(n: int) -> list[int]:
    return []
```

Run `uv run pytest`:

```
    def test_up_to_five():
>       assert count_bits(5) == [0, 1, 1, 2, 1, 2]
E       assert [] == [0, 1, 1, 2, 1, 2]
E         Right contains 6 more items, first extra item: 0
```

The empty list fails everything, including `test_zero`, which wants `[0]` and not `[]`. Good, the
shape is wrong and the values are missing, exactly what we expect from a stub.

### Write enough code to make it pass

Build the answer left to right. For each `i`, shift off the last bit with `i >> 1` to get a smaller
number whose count we've already filled in, then add back `i & 1`, which is that last bit (`1` if
`i` is odd, `0` if even).

```python
from __future__ import annotations


def count_bits(n: int) -> list[int]:
    result = [0] * (n + 1)
    for i in range(1, n + 1):
        result[i] = result[i >> 1] + (i & 1)
    return result
```

The tests pass.

The recurrence is `result[i] = result[i >> 1] + (i & 1)`. Read it as: the bits of `i` are the bits
of `i` without its last digit, plus that last digit. Since `i >> 1 < i`, the value we need is
always already computed, so each entry is one lookup and one add. **That turns a per-element
log-time count into a single pass with O(1) work per element.** We start the loop at `1` because
`result[0]` is already `0` from the list we allocated, and zero has no set bits.

### Refactor

Nothing to tidy, but it's worth naming what just happened: this is dynamic programming wearing a
bitwise hat. Each answer is built from a strictly smaller one we stored earlier, which is the same
"reuse the subproblem" shape you'll see all through the DP chapters. The bit trick is just how we
pick the subproblem: lop off the last bit. (`i & ~1` would also drop the lowest bit, but here
`i >> 1` is what we want, because it gives us the *index* of the already-solved entry.)

## Wrapping up

- **An `int` is a bit array you can index and edit** with `&`, `|`, `^`, `<<`, and `>>`. When a
  problem is about which bits are set, go bitwise.
- **XOR cancels pairs** (`a ^ a == 0`), which finds the one unpaired element in O(1) space.
- **`x & (x - 1)` clears the lowest set bit**, so looping on it counts set bits in time
  proportional to how many there are, not the width of the word.
- **`x & -x` isolates the lowest set bit** and `x & (1 << i)` tests bit `i`, the two moves for
  reading individual bits.
- **Bit counts have a one-line recurrence**, `count(i) == count(i >> 1) + (i & 1)`, which is
  dynamic programming reusing a smaller subproblem.

Next: [Math](math.md), where a few number-theory tricks (gcd, modular arithmetic, digit
manipulation) play the same role that these bit tricks do here.
