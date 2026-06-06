# Backtracking

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/code/backtracking)**

Backtracking is depth-first search over the tree of partial answers. You make a choice, recurse to
explore where it leads, then undo the choice so the next one starts from a clean slate. The whole
chapter is that one rhythm, *choose / explore / un-choose*, pointed at three different problems.

## When to reach for backtracking

The signal is a problem that asks you to build every arrangement of something and the arrangements
grow by adding one piece at a time. Reach for it when:

- You're asked for **all** subsets, permutations, or combinations, not a single best one. The
  answer is a list of lists, and you assemble each one piece by piece.
- A valid answer is built from a sequence of choices, and a partial answer can be **pruned** the
  moment it goes out of bounds (the running sum overshoots, the parentheses stop balancing).
- The search space is a tree: at each node you have a handful of next moves, and you want to walk
  every root-to-leaf path.

The cost is exponential by nature, because the answers are exponential. What backtracking buys you
is that you never hold more than one path in memory at a time, and pruning lets you abandon a dead
branch before you've paid for the whole subtree under it.

## The template

The reusable skeleton lives in [`backtracking/_template.py`](backtracking/_template.py). It ships
two concrete generators that show the shape. Here's `subsets`, which builds the power set:

```python
def subsets(items: Sequence[T]) -> list[list[T]]:
    """Every subset (the power set), built by choosing to include each index or not."""
    result: list[list[T]] = []
    path: list[T] = []

    def dfs(start: int) -> None:
        result.append(path[:])  # every node is a valid subset
        for i in range(start, len(items)):
            path.append(items[i])  # choose
            dfs(i + 1)  # explore
            path.pop()  # un-choose

    dfs(0)
    return result
```

`path` is the partial answer we're building, shared across the whole recursion. The three lines in
the loop are the entire pattern: `append` to make a choice, `dfs` to explore everything that follows
from it, `pop` to take it back. That `pop` is the *backtrack*, and it's the line beginners forget.
Without it `path` keeps growing and every answer is wrong.

Two details worth naming. We append `path[:]`, a **copy**, not `path` itself, because `path` is a
single list we keep mutating; if we stored the live reference, every entry in `result` would end up
pointing at the same emptied-out list. And the `start` index means each subset only looks forward,
so we get `[1, 2]` but never also `[2, 1]`, since for subsets order doesn't matter.

The other generator, `permutations`, keeps a `used` array instead of a `start` index, because for
orderings order *does* matter and every unused element is a legal next choice:

```python
def dfs() -> None:
    if len(path) == len(items):  # leaf: a complete permutation
        result.append(path[:])
        return
    for i in range(len(items)):
        if used[i]:
            continue
        used[i] = True  # choose
        path.append(items[i])
        dfs()  # explore
        path.pop()
        used[i] = False  # un-choose
```

Same rhythm, and notice the choose/un-choose now flips two things in lockstep: `used[i]` and `path`.
**Whatever you mutate on the way down, you undo on the way back up.** Keep that pairing tight and the
rest is bookkeeping.

The template's own tests live in [`backtracking/test_template.py`](backtracking/test_template.py) and
pin down the easy-to-miss edges: `subsets([])` is `[[]]` (the empty set still has one subset, the
empty one), and three distinct items give eight subsets and six permutations. Run `uv run pytest`
and they're green. Now let's solve some real problems with this skeleton.

## Problem 1: Combination Sum

> Given a list of distinct positive integers `candidates` and a `target`, return every combination
> that sums to `target`. You may reuse a candidate as many times as you like. Order within a
> combination doesn't matter.

This is `subsets` with two twists: we stop at a target instead of collecting every node, and we're
allowed to pick the same number again. Both twists are one-line changes to the template.

### Write the test first

```python
from combination_sum import combination_sum


def _normalise(result):
    return sorted(sorted(combo) for combo in result)


def test_reuse_allowed():
    result = combination_sum([2, 3, 6, 7], 7)
    assert _normalise(result) == _normalise([[2, 2, 3], [7]])


def test_many_combinations():
    result = combination_sum([2, 3, 5], 8)
    assert _normalise(result) == _normalise([[2, 2, 2, 2], [2, 3, 3], [3, 5]])


def test_no_combination():
    assert combination_sum([2], 1) == []


def test_single_candidate_equals_target():
    assert combination_sum([5], 5) == [[5]]


def test_target_zero():
    assert combination_sum([2, 3], 0) == [[]]
```

The problem says order doesn't matter, so we compare through `_normalise`, which sorts the numbers
inside each combination and then sorts the combinations. That way the test doesn't care what order
our search happens to emit. `test_reuse_allowed` is the one that earns its keep: `[2, 2, 3]` is only
legal because we can take the `2` twice. `test_target_zero` pins the base case, an empty combination
sums to zero, so the one and only answer is `[[]]`.

### Try to run the test

The module doesn't exist yet, so the import is the first thing to break:

```
ImportError: cannot import name 'combination_sum' from 'backtracking.solutions.combination_sum'
```

Listen to the error. It's telling us exactly which name to define and where.

### Write the minimal amount of code for the test to run and check the failing test output

Give it a `combination_sum` that returns an empty list. We're not solving anything yet; we just want
the test to run so we can watch it fail on the values and prove the test checks what we think.

```python
from __future__ import annotations


def combination_sum(candidates, target):
    return []
```

Run `uv run pytest`:

```
FF.FF
______________________________ test_reuse_allowed ______________________________

    def test_reuse_allowed():
        result = combination_sum([2, 3, 6, 7], 7)
>       assert _normalise(result) == _normalise([[2, 2, 3], [7]])
E       assert [] == [[2, 2, 3], [7]]
E         Right contains 2 more items, first extra item: [2, 2, 3]
```

Four fail on the value, and `test_no_combination` passes because `[2]` really has no combination
summing to `1`, so an empty list is the right answer by accident. The stub is wrong for the right
reason on the other four. Good, now let's make them all pass for the right reason.

### Write enough code to make it pass

Carry a `remaining` down the recursion instead of re-summing the path each time. When `remaining`
hits zero we've found a combination. The reuse twist is a single character: we recurse with `i`
instead of `i + 1`, so the same candidate is still on the table next time.

```python
from __future__ import annotations


def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    result: list[list[int]] = []
    path: list[int] = []

    def dfs(start: int, remaining: int) -> None:
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            choice = candidates[i]
            if choice > remaining:
                continue
            path.append(choice)  # choose
            dfs(i, remaining - choice)  # explore (i, not i + 1: reuse allowed)
            path.pop()  # un-choose

    dfs(0, target)
    return result
```

The tests pass.

Two things are carrying their weight here. The `if choice > remaining: continue` is the **pruning**:
a candidate bigger than what's left can't help, so we don't even open that branch. And recursing with
`start = i` rather than `i + 1` is what allows reuse while still forbidding `[3, 2]` after `[2, 3]`,
because we only ever look forward from where we are. That keeps each combination in non-decreasing
order and stops us emitting the same set twice.

### Refactor

There's little to tidy in a dozen lines, but it's worth seeing how close this stayed to `subsets`.
We kept the `start` index, kept the choose/explore/un-choose trio, and changed exactly two things:
the leaf test became `remaining == 0` instead of "every node", and the recursive call passes `i` so a
choice can repeat. **The template bends to the problem; the rhythm doesn't change.** Re-run the tests
to confirm nothing moved.

## Problem 2: Generate Parentheses

> Given `n` pairs of parentheses, return every string of `n` opening and `n` closing brackets that
> is well-formed.

Here there's no list of items to pick from. The choices at each step are baked into the rules: you
may add a `(` if you haven't used all `n` opens, and you may add a `)` if it would close an open
bracket that's still hanging. That second rule is the prune that keeps every string we build valid.

### Write the test first

```python
from generate_parentheses import generate_parentheses


def test_n_zero():
    assert generate_parentheses(0) == [""]


def test_n_one():
    assert generate_parentheses(1) == ["()"]


def test_n_two():
    assert sorted(generate_parentheses(2)) == sorted(["(())", "()()"])


def test_n_three():
    expected = ["((()))", "(()())", "(())()", "()(())", "()()()"]
    assert sorted(generate_parentheses(3)) == sorted(expected)


def test_count_is_catalan():
    # The number of valid strings for n pairs is the nth Catalan number: 1, 1, 2, 5, 14.
    assert len(generate_parentheses(4)) == 14
```

`test_n_zero` says zero pairs still produce one string, the empty one. `test_count_is_catalan` is a
cheap sanity net: the valid strings for `n` pairs are counted by the Catalan numbers, so getting
`14` for `n = 4` is strong evidence we're neither dropping valid strings nor inventing bad ones.

### Try to run the test

Nothing to import yet:

```
ImportError: cannot import name 'generate_parentheses' from 'backtracking.solutions.generate_parentheses'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return an empty list so the tests run:

```python
from __future__ import annotations


def generate_parentheses(n):
    return []
```

Run `uv run pytest`:

```
FFFFF
_________________________________ test_n_zero __________________________________

    def test_n_zero():
>       assert generate_parentheses(0) == [""]
E       AssertionError: assert [] == ['']
E         Right contains one more item: ''
```

All five fail on the value, including `n = 0`, which is what we want: even the empty case expects a
real answer, `[""]`, not `[]`. The stub is honestly wrong everywhere.

### Write enough code to make it pass

Track two counters as we recurse: how many opens we've placed and how many closes. We're done when
`path` has all `2 * n` characters. The two rules become two guarded branches.

```python
from __future__ import annotations


def generate_parentheses(n: int) -> list[str]:
    result: list[str] = []
    path: list[str] = []

    def dfs(open_count: int, close_count: int) -> None:
        if len(path) == 2 * n:
            result.append("".join(path))
            return
        if open_count < n:
            path.append("(")  # choose
            dfs(open_count + 1, close_count)  # explore
            path.pop()  # un-choose
        if close_count < open_count:
            path.append(")")
            dfs(open_count, close_count + 1)
            path.pop()

    dfs(0, 0)
    return result
```

Green, all five.

The `close_count < open_count` guard is the whole game. It refuses to add a `)` unless there's an
unmatched `(` waiting for it, so we never build an invalid prefix like `)(` and never have to throw a
finished string away. That's pruning at its best: an illegal branch is never entered, so we do zero
wasted work. And because we only emit a string when `len(path) == 2 * n`, every string we collect is
already balanced by construction.

### Refactor

The two branches still follow choose/explore/un-choose, just expressed as two `if`s instead of a
`for` loop, because the choices here aren't "the items in a list", they're "the two bracket types,
each legal under a condition". Naming the counters `open_count` and `close_count` is the readability
win; you can read the guards aloud and they're the rules of the problem. No structural change needed,
so re-run the tests and move on.

## Problem 3: Letter Combinations of a Phone Number

> Given a string of digits `2` through `9`, return every letter string you could type on an old
> phone keypad, where each digit maps to its letters (`2` to `abc`, `3` to `def`, and so on).

This is the cleanest backtrack of the three. Each position in the answer comes from one digit, and
the choices at that position are exactly that digit's letters. No pruning, no reuse, just walk the
digits left to right and branch on the letters.

### Write the test first

```python
from letter_combinations import letter_combinations


def test_empty_returns_empty_list():
    assert letter_combinations("") == []


def test_single_digit():
    assert letter_combinations("2") == ["a", "b", "c"]


def test_two_digits():
    expected = ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
    assert letter_combinations("23") == expected


def test_digit_with_four_letters():
    assert letter_combinations("7") == ["p", "q", "r", "s"]


def test_count_is_product_of_branching():
    # "79" has 4 letters then 4 letters, so 4 * 4 = 16 combinations.
    assert len(letter_combinations("79")) == 16
```

`test_empty_returns_empty_list` is a real trap: an empty input gives `[]`, not `[""]`. There are no
letters to type, so there are no combinations, and that's different from "one combination, the empty
string". `test_digit_with_four_letters` makes sure we didn't hardcode three letters per digit; `7`
and `9` carry four.

### Try to run the test

```
ImportError: cannot import name 'letter_combinations' from 'backtracking.solutions.letter_combinations'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return an empty list:

```python
from __future__ import annotations


def letter_combinations(digits):
    return []
```

Run `uv run pytest`:

```
.FFFF
______________________________ test_single_digit _______________________________

    def test_single_digit():
>       assert letter_combinations("2") == ["a", "b", "c"]
E       AssertionError: assert [] == ['a', 'b', 'c']
E         Right contains 3 more items, first extra item: 'a'
```

The empty-input test passes (an empty list is genuinely the right answer there), and the other four
fail on their values. That one accidental pass is a fine reminder: **a single green test proves
nothing on its own.**

### Write enough code to make it pass

Map each digit to its letters once, then `dfs` over the digit positions. At position `index` we
branch on every letter for `digits[index]`. When `index` reaches the end, `path` is a complete
combination. The empty-input case is its own early return, because otherwise `dfs` would dutifully
produce `[""]`.

```python
from __future__ import annotations

DIGIT_LETTERS = {
    "2": "abc",
    "3": "def",
    "4": "ghi",
    "5": "jkl",
    "6": "mno",
    "7": "pqrs",
    "8": "tuv",
    "9": "wxyz",
}


def letter_combinations(digits: str) -> list[str]:
    if not digits:
        return []

    result: list[str] = []
    path: list[str] = []

    def dfs(index: int) -> None:
        if index == len(digits):
            result.append("".join(path))
            return
        for letter in DIGIT_LETTERS[digits[index]]:
            path.append(letter)  # choose
            dfs(index + 1)  # explore
            path.pop()  # un-choose

    dfs(0)
    return result
```

The tests pass.

This is `subsets` with the lid taken off: instead of choosing whether to include each index, we
choose *which letter* fills each position, and we only collect at the leaf (`index == len(digits)`)
rather than at every node. The early `if not digits: return []` is the one special case the recursion
can't express on its own, and the test for it is what reminded us to add it.

### Refactor

Nothing to restructure. The only judgment call is that guard at the top, and I'd keep it: pushing the
empty-input check into `dfs` would tangle the leaf logic for no gain. Re-run the tests and we're done.

## Wrapping up

- **Backtracking is DFS that builds answers by choosing, exploring, then un-choosing.** The `pop`
  that undoes a choice is the line that makes it work, and the line that's easiest to forget.
- **Append a copy of the path** (`path[:]`) when you collect, because the path itself keeps mutating
  under you.
- **Whatever you mutate going down, undo coming back up**, and keep paired mutations (`used[i]` and
  `path`) in lockstep.
- **Pruning is where the speed lives.** Skip a candidate that overshoots, refuse a `)` with no open
  to match: an illegal branch you never enter costs you nothing.
- The same skeleton solved a sum target, a grammar of brackets, and a phone keypad. **The choices and
  the leaf test change; the choose/explore/un-choose rhythm doesn't.**

Next: [Dynamic Programming (1D)](dp-1d.md), where the same tree of choices gets memoized so you stop
re-exploring branches you've already solved.
