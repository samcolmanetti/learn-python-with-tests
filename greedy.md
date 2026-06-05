# Greedy

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/greedy)**

A greedy algorithm makes the choice that looks best right now and never takes it back. The
hard part isn't the code, which is usually one short pass. The hard part is convincing yourself
that the local choice is safe.

## When to reach for greedy

Greedy is tempting on a lot of problems and correct on fewer than you'd hope. Reach for it when:

- You can sweep the input **once**, carrying a tiny bit of state (a running balance, the
  furthest index you can reach, the last place a letter appears), and the answer falls out.
- You can make an **exchange argument**: if some optimal solution differs from your greedy
  choice, you can swap your choice in without making things worse. That argument is what
  separates a correct greedy from a plausible-looking one that fails on the third test case.

The moment you find yourself wanting to undo a past decision or weigh future possibilities, you
want dynamic programming or backtracking instead, not greedy.

## The template

There's no skeleton to import here. Unlike two pointers or prefix sum, greedy has no single
reusable shape: sometimes you sweep tracking one number, sometimes you sort first and then
sweep. So [`greedy/_template.py`](greedy/_template.py) is a note, not a function:

```python
"""Greedy has no single reusable skeleton, so this file is a note, not a template.

A greedy algorithm makes the locally best choice at each step and never revisits
it. ...

What every greedy solution shares is the obligation to argue that the local choice
is safe, that taking it never blocks a better global answer. That argument is the
real work. The code is usually one short pass.
"""
```

So the invariant greedy maintains isn't in a shared function. It's in your head: **at every
step, the choice I'm making now can't be the reason I lose later.** Each problem below carries
its own version of that promise. Let's earn it three times.

## Problem 1: Gas Station

> There are `n` gas stations in a circle. `gas[i]` is the fuel at station `i`, and `cost[i]` is
> the fuel needed to drive from station `i` to the next. Start with an empty tank at some
> station and return the starting index that lets you drive all the way around, or `-1` if no
> start works. A valid answer is guaranteed to be unique.

### Write the test first

We'll start with the textbook example, the impossible case, and the smallest inputs we can
think of.

```python
from .gas_station import can_complete_circuit


def test_simple_circuit():
    gas = [1, 2, 3, 4, 5]
    cost = [3, 4, 5, 1, 2]
    assert can_complete_circuit(gas, cost) == 3


def test_impossible_circuit():
    gas = [2, 3, 4]
    cost = [3, 4, 3]
    assert can_complete_circuit(gas, cost) == -1


def test_single_station_enough():
    assert can_complete_circuit([5], [4]) == 0


def test_single_station_not_enough():
    assert can_complete_circuit([3], [4]) == -1


def test_start_at_zero():
    gas = [5, 1, 2, 3, 4]
    cost = [4, 4, 1, 5, 1]
    assert can_complete_circuit(gas, cost) == 4


def test_exact_balance():
    gas = [2, 2, 2]
    cost = [2, 2, 2]
    assert can_complete_circuit(gas, cost) == 0
```

`test_impossible_circuit` pins the `-1` path, and `test_exact_balance` checks the knife-edge
where total gas exactly equals total cost.

### Try to run the test

The function doesn't exist yet, so the import is the first thing to break:

```
ImportError: cannot import name 'can_complete_circuit' from 'greedy.solutions.gas_station'
```

Listen to the error. It's telling us where to start.

### Write the minimal amount of code for the test to run and check the failing test output

Give it a `can_complete_circuit` that always gives up and returns `-1`. We're not solving
anything yet. We just want the tests to run so we can watch them fail on the value.

```python
from __future__ import annotations


def can_complete_circuit(gas: list[int], cost: list[int]) -> int:
    return -1
```

Run `uv run pytest`:

```
    def test_simple_circuit():
        gas = [1, 2, 3, 4, 5]
        cost = [3, 4, 5, 1, 2]
>       assert can_complete_circuit(gas, cost) == 3
E       assert -1 == 3
E        +  where -1 = can_complete_circuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2])
```

Four fail on the value, two pass because they happen to expect `-1`. That's the stub getting
lucky, not the logic working. Now let's make them all pass for the right reason.

### Write enough code to make it pass

Two ideas do the whole job.

First, the feasibility check: if the total gas is less than the total cost, no start can finish,
so return `-1`. If the totals are equal or gas wins, a valid start exists.

Second, the greedy choice for finding it. Walk the stations keeping a running `tank` of net
fuel (`gas[i] - cost[i]`). The instant `tank` goes negative, no station from the current `start`
through `i` could have been the answer, so jump `start` to `i + 1` and reset the tank to zero.

```python
from __future__ import annotations


def can_complete_circuit(gas: list[int], cost: list[int]) -> int:
    if sum(gas) < sum(cost):
        return -1

    start = 0
    tank = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:
            start = i + 1
            tank = 0
    return start
```

Run the tests again and they're green.

Here's the exchange argument, because this is the kind of greedy that looks like a guess until
you see why it holds. Suppose the tank goes negative at station `i` while starting from `start`.
Then no station `j` between `start` and `i` could be a valid start either: the run from `start`
to `j` was non-negative (otherwise we'd have reset earlier), so starting at `j` gives you *less*
fuel reaching `i`, not more. Every candidate in that stretch fails for the same reason, so
skipping all of them to `i + 1` is safe. And once we know a solution exists (the totals told us
so), the one start that never dips is the answer.

### Refactor

There's little to tidy in nine lines, but it's worth naming what we avoided. The naive solution
tries every start and simulates a full loop from each, which is O(n^2). We made one pass for the
totals and one pass for the start, so it's O(n) time and O(1) extra space. Two passes, no
backtracking, no second-guessing. Re-run the tests to confirm nothing moved.

## Problem 2: Jump Game

> You're given an array `nums` where `nums[i]` is the maximum jump length from index `i`.
> Starting at index `0`, return `True` if you can reach the last index, `False` otherwise.

### Write the test first

The interesting cases are a `0` that traps you and a `0` you can leap straight over.

```python
from .jump_game import can_jump


def test_reachable():
    assert can_jump([2, 3, 1, 1, 4]) is True


def test_blocked_by_zero():
    assert can_jump([3, 2, 1, 0, 4]) is False


def test_single_element():
    assert can_jump([0]) is True


def test_leading_zero_with_more():
    assert can_jump([0, 1]) is False


def test_exact_jumps():
    assert can_jump([1, 1, 1, 1]) is True


def test_big_first_jump():
    assert can_jump([5, 0, 0, 0, 0]) is True
```

`test_single_element` is the easy-to-miss one: you start on the last index, so you've already
arrived. And `test_big_first_jump` proves a single big jump clears a field of zeros that would
otherwise each be a dead end.

### Try to run the test

Same as before, no function yet:

```
ImportError: cannot import name 'can_jump' from 'greedy.solutions.jump_game'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to always say no:

```python
from __future__ import annotations


def can_jump(nums: list[int]) -> bool:
    return False
```

Run `uv run pytest`:

```
    def test_reachable():
>       assert can_jump([2, 3, 1, 1, 4]) is True
E       assert False is True
E        +  where False = can_jump([2, 3, 1, 1, 4])
```

Failing on the value, exactly as we want before writing the real thing.

### Write enough code to make it pass

The greedy move is to track the furthest index we can `reach` as we sweep. At each index `i`,
if `i` is already past everything we could reach, we're stuck and the answer is `False`.
Otherwise we extend `reach` to `max(reach, i + nums[i])` and keep going. Reach the end of the
loop and we made it.

```python
from __future__ import annotations


def can_jump(nums: list[int]) -> bool:
    reach = 0
    for i, step in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + step)
    return True
```

The tests pass.

Why is one number enough? Because reachability is contiguous: if you can reach index `i`, you
can reach every index before it too. So we never need to know *which* path got us here, only how
far forward we can possibly get. The greedy choice (always stretch `reach` as far as this index
allows) can't cost us anything, because a longer reach can only ever help. That's the safety
argument that makes the single variable legitimate.

### Refactor

Nothing to restructure. I want to flag one thing for the reader though: we never built a table
of "can I reach index `i`" the way a dynamic-programming solution would. That DP is correct but
O(n^2) in the worst case; tracking a single frontier is O(n) time and O(1) space. **When a DP
state collapses to one running number, you've usually found a greedy.** Re-run the tests.

## Problem 3: Partition Labels

> Given a string `s`, partition it into as many parts as possible so that each letter appears in
> at most one part. Return a list of the sizes of those parts, in order.

### Write the test first

```python
from .partition_labels import partition_labels


def test_classic_example():
    assert partition_labels("ababcbacadefegdehijhklij") == [9, 7, 8]


def test_single_char():
    assert partition_labels("a") == [1]


def test_all_same():
    assert partition_labels("aaaa") == [4]


def test_all_distinct():
    assert partition_labels("abcde") == [1, 1, 1, 1, 1]


def test_empty():
    assert partition_labels("") == []


def test_one_big_partition():
    assert partition_labels("abccba") == [6]
```

`test_all_distinct` and `test_one_big_partition` are the two extremes: every letter its own
part, versus the whole string forced into one part because the first and last letters match.

### Try to run the test

```
ImportError: cannot import name 'partition_labels' from 'greedy.solutions.partition_labels'
```

### Write the minimal amount of code for the test to run and check the failing test output

Return an empty list so the tests run:

```python
from __future__ import annotations


def partition_labels(s: str) -> list[int]:
    return []
```

Run `uv run pytest`:

```
    def test_classic_example():
>       assert partition_labels("ababcbacadefegdehijhklij") == [9, 7, 8]
E       assert [] == [9, 7, 8]
E         
E         Right contains 3 more items, first extra item: 9
```

The empty-string test passes by luck (its expected answer really is `[]`), the rest fail on the
value. Now make them all pass for the right reason.

### Write enough code to make it pass

First, in one pass, record the **last** index where each letter appears. That map is the whole
trick: a part can't end before the last occurrence of any letter it contains.

Then sweep again, growing the current part's `end` to the furthest last-occurrence we've seen so
far. When the loop index `i` finally lands exactly on `end`, every letter inside the part is
fully contained, so we cut here and start the next part.

```python
from __future__ import annotations


def partition_labels(s: str) -> list[int]:
    last = {char: i for i, char in enumerate(s)}

    sizes = []
    start = 0
    end = 0
    for i, char in enumerate(s):
        end = max(end, last[char])
        if i == end:
            sizes.append(end - start + 1)
            start = i + 1
    return sizes
```

Green.

The greedy choice is "cut as soon as you legally can". When `i == end`, nothing earlier in the
part reaches past `i`, so closing the part here can't merge two letters that should stay split.
Cutting any later would only make the part bigger and the total count smaller, and we were asked
for *as many parts as possible*. Cutting earlier is illegal. So the first legal cut is always
the right one, which is the exchange argument again, dressed in different clothes.

### Refactor

The body is already tight. Worth naming the shape: this is the same skeleton as a merge of
overlapping intervals, where each letter is an interval from its first to its last index, and we
emit a part whenever the running `end` closes. We just never materialised the intervals, because
the `last` map and a single `end` variable carry everything we need. One pass to build the map,
one pass to cut, O(n) time. Re-run the tests.

## Wrapping up

- **Greedy makes the locally best choice and never revisits it.** The code is short; the proof
  that the choice is safe is the actual work.
- **The exchange argument is the tool.** Show that swapping your greedy choice into any optimal
  solution never makes it worse, and the greedy is correct. We used it three times: skip-on-empty
  for gas, stretch-the-frontier for jumps, cut-at-first-legal-point for labels.
- **Watch for a DP state that collapses to one running number** (a balance, a reach, an `end`).
  That collapse from O(n^2) to O(n) is usually the sign a greedy is hiding in the problem.
- **A common trap**: greedy *feels* right far more often than it *is* right. If you can imagine
  wanting to undo a choice, reach for dynamic programming or backtracking instead.

Next: [Intervals](intervals.md), where the cut-when-the-running-end-closes idea from partition
labels becomes the main event.
