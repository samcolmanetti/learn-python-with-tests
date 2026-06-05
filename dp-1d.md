# DP: 1D

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/dp_1d)**

Dynamic programming sounds scary and the name is no help at all. Strip the jargon and 1D DP is
just this: you've got a problem whose answer for size `n` is built from the answers for a few
smaller sizes. Work out the answers for the small cases, write them in a table, and fill the rest
left to right. The reusable skeleton lives in [`dp_1d/_template.py`](dp_1d/_template.py) and the
worked problems in `dp_1d/solutions/`, each built test-first.

## When to reach for 1D DP

The tell is a problem where a brute-force recursion would re-solve the same subproblem over and
over. Reach for a 1D table when:

- You can describe the state with **one index**, `i`, and the answer `dp[i]` depends only on a
  fixed handful of earlier entries (`dp[i - 1]`, `dp[i - 2]`, and so on). That fixed handful is
  the *transition*.
- You're being asked to **count ways**, find a **min or max over choices**, or decide
  **reachability** along a sequence, and the choice at step `i` only cares about a few steps
  behind it.

If the recursion would branch into `f(i - 1)` and `f(i - 2)` and those overlap, a table kills the
re-computation. That's the whole game.

## The template

```python
from collections.abc import Callable


def bottom_up(n, base, transition):
    if n < len(base):
        return base[n]
    dp = base + [0] * (n + 1 - len(base))
    for i in range(len(base), n + 1):
        dp[i] = transition(dp, i)
    return dp[n]
```

Three moving parts. `base` is the list of answers you already know without any work, the small
cases at the front of the table. `transition(dp, i)` is the rule that builds `dp[i]` from entries
already filled. The loop applies the rule from the first unknown index up to `n`, and the answer
is the last cell `dp[n]`.

We size the table to `n + 1` so `dp[0]` has a home. The *invariant* the loop maintains is that
when we compute `dp[i]`, every entry it reads (`dp[i - 1]`, `dp[i - 2]`, ...) is already correct.
Fill the table in increasing order of `i` and that holds for free.

You won't usually call `bottom_up` directly in an interview. It's here to name the shape. Every
solution below is this exact pattern with a different `base` and `transition`, and most of the
time we'll inline it and then notice we only need the last two cells, not the whole table.

## Problem 1: Climbing Stairs

> You can climb 1 or 2 steps at a time. How many distinct ways are there to reach the top of a
> staircase with `n` steps?

To land on step `i`, your last move was either a single step from `i - 1` or a double step from
`i - 2`. So the ways to reach `i` are the ways to reach `i - 1` plus the ways to reach `i - 2`.
That's `dp[i] = dp[i - 1] + dp[i - 2]`, which you might recognise as Fibonacci wearing a hat.

### Write the test first

```python
from .climbing_stairs import climb_stairs


def test_zero_steps():
    assert climb_stairs(0) == 1


def test_one_step():
    assert climb_stairs(1) == 1


def test_two_steps():
    assert climb_stairs(2) == 2


def test_three_steps():
    assert climb_stairs(3) == 3


def test_five_steps():
    assert climb_stairs(5) == 8


def test_larger_input():
    assert climb_stairs(45) == 1836311903
```

The base cases need care. `climb_stairs(0)` is `1`, not `0`: there's exactly one way to stand
still, the empty climb. Getting that wrong throws off every later entry, so we pin it down first.
`test_larger_input` is there to catch a solution that's accidentally exponential. If you wrote the
naive recursion it would still be churning when the interviewer's patience runs out.

### Try to run the test

We've imported `climb_stairs` from a module that doesn't define it yet, so the import is what
breaks first:

```
E   ImportError: cannot import name 'climb_stairs' from 'dp_1d.solutions.climbing_stairs'
```

No function, nothing to call. The error is pointing us at the next move.

### Write the minimal amount of code for the test to run and check the failing test output

Give it a `climb_stairs` that returns a stub `0`. We're not solving anything yet, we just want
the test to run so we can watch it fail on the value. That proves the test is checking what we
think it is.

```python
from __future__ import annotations


def climb_stairs(n: int) -> int:
    return 0
```

Run `uv run pytest`:

```
    def test_zero_steps():
>       assert climb_stairs(0) == 1
E       assert 0 == 1
E        +  where 0 = climb_stairs(0)
```

```
6 failed in 0.11s
```

Every test fails on the value, not on a missing name. That's exactly the signal we want before
writing the real thing.

### Write enough code to make it pass

We could allocate the whole `dp` table, but the transition only ever reads the last two entries,
so we carry two numbers instead of a list. `prev` is `dp[i - 2]`, `curr` is `dp[i - 1]`, and each
step slides them forward.

```python
from __future__ import annotations


def climb_stairs(n: int) -> int:
    if n <= 1:
        return 1
    prev, curr = 1, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr
```

The tests pass.

The `n <= 1` guard handles both base cases at once: zero steps and one step each have a single
way. After that the loop runs `n - 1` times, doing one addition each, so this is O(n) time and
O(1) space.

### Refactor

There's nothing to tidy in seven lines, but it's worth naming what happened. We started from the
template's `dp[i] = dp[i - 1] + dp[i - 2]` and then noticed the transition has a *window* of two,
so the full table was wasteful. **Carrying just the cells the transition reads is the standard
1D-DP space optimisation**, and it works whenever your window is a fixed size. Re-run the tests to
confirm the rolling variables didn't break anything.

## Problem 2: House Robber

> Houses sit in a row, each holding some money. You can't rob two adjacent houses or the alarms
> go off. Return the most money you can take.

Now the transition has a choice in it, not just a sum. Standing at house `i`, you either skip it
(and keep whatever you'd robbed up to `i - 1`) or rob it (taking its money plus whatever you'd
robbed up to `i - 2`, since `i - 1` is now off-limits). You want the better of the two, so
`dp[i] = max(dp[i - 1], nums[i] + dp[i - 2])`.

### Write the test first

```python
from .house_robber import rob


def test_empty():
    assert rob([]) == 0


def test_single_house():
    assert rob([5]) == 5


def test_two_houses_take_larger():
    assert rob([2, 7]) == 7


def test_skip_middle():
    assert rob([1, 2, 3, 1]) == 4


def test_alternating_big():
    assert rob([2, 7, 9, 3, 1]) == 12


def test_all_equal():
    assert rob([4, 4, 4, 4]) == 8
```

`test_skip_middle` is the one that earns its keep. The greedy move on `[1, 2, 3, 1]` grabs the
biggest house first, but the right answer robs house `0` and house `2` for `1 + 3 = 4`, which
beats robbing the lone `3`. A solution that just picks the largest non-adjacent values one at a
time gets this wrong, so we want it in the suite from the start.

### Try to run the test

The function doesn't exist yet, so the import fails first:

```
E   ImportError: cannot import name 'rob' from 'dp_1d.solutions.house_robber'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub `rob` to return `0` so the tests run:

```python
from __future__ import annotations


def rob(nums: list[int]) -> int:
    return 0
```

Run `uv run pytest`:

```
    def test_single_house():
>       assert rob([5]) == 5
E       assert 0 == 5
E        +  where 0 = rob([5])
```

```
5 failed, 1 passed in 0.11s
```

One test passes: `test_empty`, because an empty row really does net `0`, which is what our stub
happens to return. The other five fail on the value. **A green test next to a stub that returns a
constant proves nothing on its own**, it just means the expected value matched the constant. Now
let's make all six pass for the right reason.

### Write enough code to make it pass

Same trick as before: the transition reads `dp[i - 1]` and `dp[i - 2]`, so we carry two running
numbers. `take` is the best take including the current house's decision, `skip` is the best take
up to the previous house.

```python
from __future__ import annotations


def rob(nums: list[int]) -> int:
    skip, take = 0, 0
    for value in nums:
        skip, take = take, max(take, skip + value)
    return take
```

The tests pass.

Read the loop body carefully. Before the line runs, `take` is the best for houses up to `i - 1`
and `skip` is the best up to `i - 2`. The new `take` is `max(take, skip + value)`: skip this
house and keep the old best, or rob it and add its money to the best-from-two-back. The new `skip`
becomes the old `take`, sliding the window forward. Starting both at `0` gives the empty-row and
single-house base cases for free, which is why we didn't need a special branch.

### Refactor

None needed. This is the same rolling-window shape as climbing stairs, with the transition's `+`
swapped for a `max` over two choices. That swap is the whole difference between *counting* DP and
*optimising* DP. **When the transition is a `max` or `min` over a small set of choices, you're
optimising; when it's a sum, you're counting.** Re-run the tests and move on.

## Problem 3: Coin Change

> Given coin denominations and a target `amount`, return the fewest coins that sum to it, or `-1`
> if no combination of coins works.

The window stops being a fixed two here, and that's the point of including it. The state is still
one index, the amount `a`, and `dp[a]` is the fewest coins that make `a`. But the transition looks
at `dp[a - coin]` for *every* coin, not a fixed offset: whichever coin you spend last, the rest
must make `a - coin`. So `dp[a] = min(1 + dp[a - coin] for coin in coins if coin <= a)`.

The `-1` rule needs handling too. Some amounts can't be made at all, and we have to tell those
apart from amounts we just haven't filled yet.

### Write the test first

```python
from .coin_change import coin_change


def test_simple_combination():
    assert coin_change([1, 2, 5], 11) == 3


def test_impossible():
    assert coin_change([2], 3) == -1


def test_zero_amount():
    assert coin_change([1], 0) == 0


def test_exact_single_coin():
    assert coin_change([1, 2, 5], 5) == 1


def test_prefers_fewer_coins():
    assert coin_change([1, 3, 4], 6) == 2


def test_no_coins_nonzero_amount():
    assert coin_change([], 7) == -1
```

`test_prefers_fewer_coins` is the case that punishes greed. Grabbing the biggest coin first on
`[1, 3, 4]` for `6` gives `4 + 1 + 1`, three coins, but `3 + 3` is two. DP considers every last
coin and finds the two-coin answer. `test_impossible` and `test_no_coins_nonzero_amount` pin down
the `-1` path so we can't fake it with a sum.

### Try to run the test

Nothing to import yet:

```
E   ImportError: cannot import name 'coin_change' from 'dp_1d.solutions.coin_change'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return `0` so the tests run:

```python
from __future__ import annotations


def coin_change(coins: list[int], amount: int) -> int:
    return 0
```

Run `uv run pytest`:

```
    def test_simple_combination():
>       assert coin_change([1, 2, 5], 11) == 3
E       assert 0 == 3
E        +  where 0 = coin_change([1, 2, 5], 11)
```

```
5 failed, 1 passed in 0.10s
```

`test_zero_amount` passes because making `0` really does take zero coins, and the stub returns
`0`. Same lesson as last time: that pass is a coincidence, not a solution. The other five fail on
the value.

### Write enough code to make it pass

We need a "not reachable yet" marker that won't accidentally win a `min`. Any real answer is at
most `amount` coins (you can't spend more coins than the amount itself when the smallest coin is
at least `1`), so `amount + 1` is a safe stand-in for infinity. We fill `dp[0] = 0` and the rest
with that marker, then relax each cell against every coin.

```python
from __future__ import annotations


def coin_change(coins: list[int], amount: int) -> int:
    unreachable = amount + 1
    dp = [0] + [unreachable] * amount
    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a:
                dp[a] = min(dp[a], 1 + dp[a - coin])
    return dp[amount] if dp[amount] != unreachable else -1
```

The tests pass.

Using `amount + 1` instead of `float("inf")` keeps every cell an `int` and means `1 + dp[a -
coin]` never overflows into nonsense. If `dp[amount]` is still the marker at the end, no
combination ever reached it, so we return `-1`. **The sentinel-for-infinity trick is how you fold
"impossible" into a `min` DP without a special case in the inner loop.** This is O(amount *
len(coins)) time and O(amount) space.

### Refactor

The double loop is already as clean as it gets, but notice this is the template stretched. The
transition no longer reads a fixed window like `dp[i - 1]` and `dp[i - 2]`, so we can't collapse
the table down to two variables. We need the whole `dp` array, because `dp[a - coin]` can reach
arbitrarily far back depending on the coin. **A fixed-size window lets you drop the array; a
variable reach forces you to keep it.** That's the line between the cheap O(1)-space problems and
the ones that need the full table. Re-run the tests to confirm nothing moved.

## Wrapping up

- **1D DP fills a table where `dp[i]` is built from a few earlier entries by a fixed transition.**
  Nail the base cases first, fill from the bottom up, and the answer is the last cell.
- **The transition tells you the flavour.** A sum counts ways (climbing stairs), a `max` or `min`
  over choices optimises (house robber, coin change).
- **A fixed-size window means you can throw the array away** and carry just the cells the
  transition reads, dropping the space to O(1). Climbing stairs and house robber both do this.
- **A variable reach forces you to keep the whole table** (coin change reads `dp[a - coin]` for
  every coin), and **a sentinel like `amount + 1` folds "impossible" into a `min`** so the `-1`
  case needs no special branch.

Next: [DP: Grid](dp-grid.md), where the state grows a second index and the table becomes a grid
you fill row by row.
