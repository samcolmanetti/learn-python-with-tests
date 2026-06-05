# DP: Intervals and sequences

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/dp_intervals)**

This is dynamic programming where the subproblems are indexed by *positions*: a prefix of one
string against a prefix of another, or a sub-interval of a single sequence. You fill a 2D table
bottom-up so every cell a recurrence reads is already there when you need it.

## When to reach for sequence DP

The signals are about *structure*, not keywords. Reach for a 2D table when:

- You're comparing **two sequences** and the answer for the whole pair depends on the answer for
  their prefixes. Longest common subsequence and edit distance both live here. The table is
  `(m + 1) x (n + 1)`, indexed by how much of each string you've consumed.
- You're asking about **a sub-interval** of one sequence, and a longer interval's answer follows
  from shorter ones inside it. Longest palindromic subsequence is this. The table is `n x n`,
  indexed by the interval's two endpoints, and you fill it by increasing interval length.
- The brute force is **exponential** (try every subsequence, every alignment) but there are only
  O(n * m) distinct subproblems. That gap between exponential choices and polynomial subproblems
  is exactly what DP collapses.

The whole game is picking the right index for your table and writing the recurrence that relates a
cell to its neighbours. Once those two are right, the loop that fills the table almost writes
itself.

## The template

Most of these problems share a shape: allocate a grid, fill its base row and column with the
empty-prefix answers, then fill each interior cell from cells already computed. Here's that
skeleton.

```python
from collections.abc import Callable, Sequence
from typing import TypeVar

T = TypeVar("T")


def fill_grid(
    a: Sequence[T],
    b: Sequence[T],
    base: Callable[[int, int], int],
    step: Callable[[list[list[int]], int, int], int],
) -> list[list[int]]:
    m, n = len(a), len(b)
    table = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        table[i][0] = base(i, 0)
    for j in range(n + 1):
        table[0][j] = base(0, j)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            table[i][j] = step(table, i, j)
    return table
```

The invariant is the part worth memorising: **when you fill `table[i][j]`, the three cells it can
depend on (`table[i-1][j]`, `table[i][j-1]`, `table[i-1][j-1]`) are already filled.** The loop
order, rows outer and columns inner, guarantees it. The leading row and column (`i == 0` or
`j == 0`) stand for "one of the prefixes is empty", and those are your base cases.

I won't import `fill_grid` in the solutions below. The base case and the recurrence change per
problem, and inlining the loop reads clearer than threading two callbacks through a helper. The
template is here to fix the shape in your head, not to abstract it away. The interval problem at
the end uses a different index entirely, and we'll build its table by hand.

## Problem 1: Longest Common Subsequence

> Given two strings, return the length of their longest common subsequence. A subsequence keeps
> characters in order but doesn't need them contiguous.

The brute force is "generate every subsequence of `a`, check which appear in `b`", and there are
`2^m` subsequences. That's the exponential-versus-polynomial gap from above. Let's collapse it.

### Write the test first

```python
from .longest_common_subsequence import longest_common_subsequence


def test_shared_run():
    assert longest_common_subsequence("abcde", "ace") == 3


def test_identical_strings():
    assert longest_common_subsequence("abc", "abc") == 3


def test_no_common_characters():
    assert longest_common_subsequence("abc", "def") == 0


def test_interleaved_match():
    assert longest_common_subsequence("abcba", "abcbcba") == 5


def test_empty_first():
    assert longest_common_subsequence("", "abc") == 0


def test_empty_second():
    assert longest_common_subsequence("abc", "") == 0


def test_both_empty():
    assert longest_common_subsequence("", "") == 0
```

`test_interleaved_match` is the one that earns its place. The common subsequence of `"abcba"` and
`"abcbcba"` is `"abcba"` itself, length 5, and you only get it if your recurrence is happy to
*skip* characters in either string to line the rest up. The empty-string cases pin down the base
row and column we just talked about.

### Try to run the test

The module doesn't define the function yet, so the import is the first thing to break:

```
ModuleNotFoundError: No module named 'dp_intervals.solutions.longest_common_subsequence'
```

No module, no function. The error is telling us where to start.

### Write the minimal amount of code for the test to run and check the failing test output

Give it a function that takes the arguments and returns a stub `0`. We're not solving anything
yet. We just want the test to run so we can watch it fail on the value, which proves the test
checks what we think it does.

```python
from __future__ import annotations


def longest_common_subsequence(a: str, b: str) -> int:
    return 0
```

Run `uv run pytest`:

```
    def test_shared_run():
>       assert longest_common_subsequence("abcde", "ace") == 3
E       AssertionError: assert 0 == 3
E        +  where 0 = longest_common_subsequence('abcde', 'ace')
```

The test runs and fails on the value, not on a missing name. `test_no_common_characters` and the
empty-string cases pass, but only because they happen to expect `0`, which is what our stub always
returns. That's the trap of a green test in isolation, and it's why we wrote the others.

### Write enough code to make it pass

Here's the recurrence. Let `table[i][j]` be the LCS length of the first `i` characters of `a` and
the first `j` characters of `b`. Then:

- If `a[i-1] == b[j-1]`, those two characters can both join the subsequence, so
  `table[i][j] = table[i-1][j-1] + 1`.
- Otherwise the last characters can't both be in it, so we drop one and take the better of the two:
  `table[i][j] = max(table[i-1][j], table[i][j-1])`.

The base cases (an empty prefix has no common subsequence) are already `0` from how we allocate
the grid, so there's nothing to fill in by hand.

```python
from __future__ import annotations


def longest_common_subsequence(a: str, b: str) -> int:
    m, n = len(a), len(b)
    table = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])
    return table[m][n]
```

Run the tests and they're green.

Watch the index offset: `a[i-1]` is the character we're considering when the table row is `i`,
because row `i` means "the first `i` characters", and the last of those sits at index `i-1`. That
off-by-one between table size (`m + 1`) and string index (`m`) is the single most common place to
trip in these problems. We fill the table in O(m * n) time and read the answer from the
bottom-right corner.

### Refactor

There's nothing to tidy in the algorithm, but it's worth naming the shape. This is exactly the
template's grid: a base row and column of zeros, then each interior cell computed from its three
neighbours. The `if a[i-1] == b[j-1]` branch is the `step`, and the all-zero base came for free
from the allocation. Re-run the tests to confirm nothing moved.

## Problem 2: Edit Distance

> Given two strings, return the minimum number of single-character insertions, deletions, and
> substitutions that turn the first into the second.

This is the same `(m + 1) x (n + 1)` grid as LCS, but now the base cases carry real numbers and
the recurrence minimises instead of maximises. It's the canonical "I changed one thing and three
things changed" DP, so let's see what changed.

### Write the test first

```python
from .edit_distance import edit_distance


def test_classic_horse_to_ros():
    assert edit_distance("horse", "ros") == 3


def test_substitution_chain():
    assert edit_distance("intention", "execution") == 5


def test_identical_strings():
    assert edit_distance("abc", "abc") == 0


def test_pure_insertions():
    assert edit_distance("", "abc") == 3


def test_pure_deletions():
    assert edit_distance("abc", "") == 3


def test_both_empty():
    assert edit_distance("", "") == 0


def test_single_substitution():
    assert edit_distance("cat", "cut") == 1
```

`test_pure_insertions` and `test_pure_deletions` are the ones that force the base row and column
to be right. Turning `""` into `"abc"` is three inserts, so `table[0][j] = j`. Turning `"abc"`
into `""` is three deletes, so `table[i][0] = i`. Those two lines are the whole reason this
problem needs more setup than LCS did.

### Try to run the test

Same story as before, the import fails first:

```
ModuleNotFoundError: No module named 'dp_intervals.solutions.edit_distance'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return `0` so the tests run:

```python
from __future__ import annotations


def edit_distance(a: str, b: str) -> int:
    return 0
```

Run `uv run pytest`:

```
    def test_classic_horse_to_ros():
>       assert edit_distance("horse", "ros") == 3
E       AssertionError: assert 0 == 3
E        +  where 0 = edit_distance('horse', 'ros')
```

Failing on the value. The three cases that expect `0` (identical strings, both empty) pass by
luck, exactly the same false comfort as last time.

### Write enough code to make it pass

Let `table[i][j]` be the edit distance between the first `i` characters of `a` and the first `j`
of `b`. The base cases are the insert/delete-everything answers we worked out from the tests:
`table[i][0] = i` and `table[0][j] = j`. Then for an interior cell:

- If the last characters match (`a[i-1] == b[j-1]`), they cost nothing, so
  `table[i][j] = table[i-1][j-1]`. We're free.
- Otherwise we pay 1 and take the cheapest of three edits: delete from `a` (`table[i-1][j]`),
  insert into `a` (`table[i][j-1]`), or substitute (`table[i-1][j-1]`).

```python
from __future__ import annotations


def edit_distance(a: str, b: str) -> int:
    m, n = len(a), len(b)
    table = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        table[i][0] = i
    for j in range(n + 1):
        table[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                table[i][j] = table[i - 1][j - 1]
            else:
                table[i][j] = 1 + min(
                    table[i - 1][j],      # delete from a
                    table[i][j - 1],      # insert into a
                    table[i - 1][j - 1],  # substitute
                )
    return table[m][n]
```

The tests pass.

Notice the three neighbours are the *same three* cells LCS read, just combined with `min(...) + 1`
instead of `max(...)`. **Most sequence DP is this one grid with a different recurrence bolted on
top.** Once you've built it once, the second one is muscle memory. Same O(m * n) time, same
read from the bottom-right corner.

### Refactor

The inline comments are carrying their weight here, so I'd leave them. The one thing worth pulling
out is that the matching branch sets cost to `table[i-1][j-1]` with no `+ 1`, which is what makes
two identical strings cost `0`: every character matches, we ride the diagonal, and never add. Drop
the comments or the base-case loops and a reader has to reverse-engineer that. Re-run the tests.

## Problem 3: Longest Palindromic Subsequence

> Given a string, return the length of its longest subsequence that reads the same forwards and
> backwards.

This one breaks the two-string mould. There's only one sequence, and the natural subproblem is
"what's the answer for the interval `s[i:j+1]`?" So the table is indexed by the two *endpoints* of
an interval, and we fill it by growing the interval length. This is *interval DP*, and it's worth
seeing the index change.

### Write the test first

```python
from .longest_palindromic_subsequence import longest_palindromic_subsequence


def test_classic_bbbab():
    assert longest_palindromic_subsequence("bbbab") == 4


def test_two_char_palindrome():
    assert longest_palindromic_subsequence("cbbd") == 2


def test_single_character():
    assert longest_palindromic_subsequence("a") == 1


def test_already_a_palindrome():
    assert longest_palindromic_subsequence("racecar") == 7


def test_no_repeats():
    assert longest_palindromic_subsequence("abcd") == 1


def test_empty():
    assert longest_palindromic_subsequence("") == 0
```

`test_classic_bbbab` is the headline: the answer is `"bbbb"`, length 4, which you only find by
*skipping* the `"a"`. `test_no_repeats` checks the floor (any single character is a palindrome of
length 1), and `test_empty` is the one case where there's no character to fall back on, so the
answer is 0.

### Try to run the test

The import fails first, as it always does:

```
ModuleNotFoundError: No module named 'dp_intervals.solutions.longest_palindromic_subsequence'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return `0`:

```python
from __future__ import annotations


def longest_palindromic_subsequence(s: str) -> int:
    return 0
```

Run `uv run pytest`:

```
    def test_classic_bbbab():
>       assert longest_palindromic_subsequence("bbbab") == 4
E       AssertionError: assert 0 == 4
E        +  where 0 = longest_palindromic_subsequence('bbbab')
```

`test_empty` passes (it wants `0`); everything with an actual palindrome in it fails on the value.
Exactly the failure we want before writing the real thing.

### Write enough code to make it pass

Let `table[i][j]` be the longest palindromic subsequence of `s[i:j+1]`. The recurrence reasons
from the two ends inward:

- Every single character is a palindrome of length 1, so `table[i][i] = 1`. That's the base case,
  and it's a diagonal this time, not a row and column.
- If the endpoints match (`s[i] == s[j]`), they wrap a palindrome around whatever's best inside,
  so `table[i][j] = table[i+1][j-1] + 2`.
- If they don't match, at least one endpoint is excluded, so we drop one and take the better side:
  `table[i][j] = max(table[i+1][j], table[i][j-1])`.

The wrinkle is the loop order. Cell `table[i][j]` reads cells from *shorter* intervals
(`table[i+1][j-1]` and friends), so we must fill shorter intervals first. We iterate by `length`
from 2 up to `n`, and within each length slide `i` across the string.

```python
from __future__ import annotations


def longest_palindromic_subsequence(s: str) -> int:
    n = len(s)
    if n == 0:
        return 0
    table = [[0] * n for _ in range(n)]
    for i in range(n):
        table[i][i] = 1
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                inner = table[i + 1][j - 1] if length > 2 else 0
                table[i][j] = inner + 2
            else:
                table[i][j] = max(table[i + 1][j], table[i][j - 1])
    return table[0][n - 1]
```

Green.

Two things to call out. The `if length > 2 else 0` guards a length-2 interval like `"bb"`: the
"inside" would be `table[i+1][j-1]` where `i+1 > j-1`, an empty interval that should contribute 0,
and we don't want to read a garbage cell for it. And the answer lives at `table[0][n-1]`, the full
interval from the first character to the last, not in the bottom-right corner like the grid
problems. **Different index, different place to read the answer.** The shape still costs O(n^2)
time and space.

### Refactor

There's a neat fact hiding here: the longest palindromic subsequence of `s` is just the longest
common subsequence of `s` and its reverse. We could delete this whole function and write
`longest_common_subsequence(s, s[::-1])`. I'm keeping the interval version anyway, because the
"grow the interval, read from `[0][n-1]`" pattern is the one you'll need for problems that *don't*
reduce to LCS (matrix-chain multiplication, burst balloons, optimal BST). The reduction is a great
thing to mention in an interview; the interval table is the thing to actually practise. Re-run the
tests.

## Wrapping up

- **Sequence DP indexes subproblems by position**: a prefix-versus-prefix grid for two strings, or
  an interval `[i, j]` for one. Pick the index first, then the recurrence falls out.
- **The dual-sequence grid is one table with a swappable recurrence.** LCS maxes over three
  neighbours, edit distance mins over the same three plus one. The leading row and column are the
  empty-prefix base cases.
- **Mind the off-by-one**: a table of size `m + 1` against a string of length `m` means
  `a[i-1]` is the character at row `i`. This is where these problems bite.
- **Interval DP fills by increasing length** so shorter intervals exist before longer ones read
  them, and the answer sits at `table[0][n-1]`, not the corner.
- **Many of these reduce to each other.** Longest palindromic subsequence is LCS of a string and
  its reverse. Knowing the reduction is interview gold; knowing the table is what saves you when
  there's no reduction.

Next: [Trie](trie.md), where the structure you build isn't a grid but a tree of shared prefixes.
