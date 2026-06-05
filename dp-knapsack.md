# DP: Knapsack

**[You can find all the code for this chapter here](https://github.com/samcolmanetti/learn-python-with-tests/tree/main/dp_knapsack)**

Knapsack is an **interview pattern**: a reusable [`dp_knapsack/_template.py`](dp_knapsack/_template.py)
plus worked problems in `dp_knapsack/solutions/`, each built test-first. You have a budget and a
pile of items, and you fill a 1D table indexed by the budget, asking one question at every cell:
am I better off skipping this item or taking it?

## When to reach for knapsack

The setup is always the same shape: a collection of items, a numeric budget, and a "best" or
"how many ways" question over which items you pick. Reach for knapsack when:

- You're choosing a **subset of items under a cap** (a weight limit, a target sum, an amount of
  money), and order doesn't matter.
- The question is "can we hit the target", "what's the most value we can fit", or "how many
  combinations reach the target".
- You can phrase each item as a yes/no (or how-many) decision, and the answer for a budget
  depends only on the answers for smaller budgets.

The one detail that splits the whole family in two is whether each item can be used **once** or
**any number of times**. That single bit decides which direction you sweep the budget, and
getting it wrong is the classic knapsack bug.

## The template

```python
def knapsack_01(costs, budget, base, take):
    dp = list(base)
    for cost in costs:
        for b in range(budget, cost - 1, -1):
            dp[b] = take(dp[b], dp[b - cost])
    return dp


def knapsack_unbounded(costs, budget, base, take):
    dp = list(base)
    for cost in costs:
        for b in range(cost, budget + 1):
            dp[b] = take(dp[b], dp[b - cost])
    return dp
```

Look at the two functions. They're identical except for one thing: the direction of the inner
`range`. That's not a coincidence, that's the entire idea.

`dp` is a table of length `budget + 1`, where `dp[b]` is the answer when the budget is exactly
`b`. We walk the items once (the outer loop), and for each item we update every budget cell with
`take(dp[b], dp[b - cost])`: keep what we had, or fold in the option of using this item, which
costs `cost` and so leaves `dp[b - cost]` behind. The `take` function is the only per-problem
piece (`max` for "best value", `a + b` for "count the ways").

The sweep direction is the whole game. In `knapsack_01` we go **high to low**, so when we read
`dp[b - cost]` it still holds the value from *before* this item was considered. That means each
item lands in `dp[b]` at most once. In `knapsack_unbounded` we go **low to high**, so by the
time we read `dp[b - cost]` it may *already* include this item, which lets us take it again.

**Same table, same "skip or take" question, opposite sweep.** Memorise that pairing: down for
0/1, up for unbounded. The rest of this chapter is three problems that each pick a sweep and a
`take`.

## Problem 1: Partition Equal Subset Sum

> Given an array of positive integers, return `True` if you can split it into two subsets with
> equal sum.

If the two halves are equal, each one sums to `total / 2`. So the real question is: can some
subset hit exactly `total / 2`? That's a 0/1 subset sum. Each number is used once or not at all,
which means a downward sweep.

### Write the test first

```python
from .partition_equal_subset_sum import can_partition


def test_even_split_exists():
    assert can_partition([1, 5, 11, 5]) is True


def test_no_split_possible():
    assert can_partition([1, 2, 3, 5]) is False


def test_odd_total_is_immediately_false():
    assert can_partition([1, 2, 5]) is False


def test_two_equal_elements():
    assert can_partition([4, 4]) is True


def test_single_element_cannot_split():
    assert can_partition([7]) is False


def test_empty_splits_into_two_empty_halves():
    assert can_partition([]) is True


def test_repeated_values():
    assert can_partition([2, 2, 2, 2, 2, 2]) is True
```

`test_odd_total_is_immediately_false` pins the cheap exit: if the total is odd, no split can be
even, and we don't even need the table. `test_empty_splits_into_two_empty_halves` is the case
people argue about in interviews, two empty subsets both sum to zero, so I've made the call that
it's `True`.

### Try to run the test

The module doesn't exist yet, so the import is the first thing to break:

```
ModuleNotFoundError: No module named 'dp_knapsack.solutions.partition_equal_subset_sum'
```

Listen to the error. It's telling us exactly which file to create.

### Write the minimal amount of code for the test to run and check the failing test output

Give it a `can_partition` that always returns `False`. We're not solving anything yet, we just
want the test to run so we can watch it fail on the value.

```python
from __future__ import annotations

from collections.abc import Sequence


def can_partition(nums: Sequence[int]) -> bool:
    return False
```

Run `uv run pytest`:

```
    def test_even_split_exists():
>       assert can_partition([1, 5, 11, 5]) is True
E       assert False is True
E        +  where False = can_partition([1, 5, 11, 5])

4 failed, 3 passed
```

The four that should be `True` fail on the value, and the three that expect `False` pass only
because `False` is what our stub hands back. That's the failure we wanted: the tests run, and
they fail for the right reason.

### Write enough code to make it pass

If the total is odd, bail early. Otherwise build a boolean table `reachable`, where
`reachable[s]` means "some subset sums to `s`". Seed `reachable[0] = True` (the empty subset
sums to zero), then sweep each number downward, marking any sum we can now reach.

```python
from __future__ import annotations

from collections.abc import Sequence


def can_partition(nums: Sequence[int]) -> bool:
    total = sum(nums)
    if total % 2 != 0:
        return False

    target = total // 2
    reachable = [False] * (target + 1)
    reachable[0] = True

    for num in nums:
        for s in range(target, num - 1, -1):
            if reachable[s - num]:
                reachable[s] = True

    return reachable[target]
```

The tests pass.

The downward sweep is doing the 0/1 work. When we check `reachable[s - num]`, that cell still
reflects the sums we could reach *without* the current `num`, so we never count the same number
twice into one subset. Flip that inner range to `range(num, target + 1)` and you'd be allowing
each number an unlimited number of times, which is a different (and wrong, here) problem.

### Refactor

There's nothing to tidy in eleven lines, but it's worth naming the shape against the template.
This is `knapsack_01`: `nums` are the costs, `target` is the budget, the base table is "only
sum 0 is reachable", and `take(current, prev)` is `current or prev` (a sum stays reachable, or
becomes reachable through this item). We inline it here because the boolean version reads more
plainly than threading a lambda, but the bones are identical. Re-run the tests to confirm
nothing moved.

## Problem 2: Coin Change II

> Given coin denominations and an `amount`, count the number of distinct combinations of coins
> that sum to `amount`. Each coin can be used any number of times.

Two things change from Problem 1. First, coins are unlimited, so this is unbounded: an upward
sweep. Second, we're *counting* combinations, not testing reachability, so `take` becomes
addition instead of "or".

There's a subtle trap in the word *combinations*. `{1, 2}` and `{2, 1}` are the same combination
and must be counted once. The loop order is what enforces that, and I'll show why.

### Write the test first

```python
from .coin_change_ii import change


def test_classic_example():
    assert change(5, [1, 2, 5]) == 4


def test_no_way_to_make_amount():
    assert change(3, [2]) == 0


def test_amount_zero_has_one_way():
    assert change(0, [1, 2, 5]) == 1


def test_no_coins_and_positive_amount():
    assert change(7, []) == 0


def test_single_coin_divides_evenly():
    assert change(10, [5]) == 1


def test_single_coin_does_not_divide():
    assert change(7, [5]) == 0


def test_combinations_are_unordered():
    # {2, 1, 1} and {1, 1, 2} are the same combination, counted once.
    assert change(4, [1, 2]) == 3
```

`test_amount_zero_has_one_way` is load-bearing: making zero has exactly one combination, the
empty one, and that empty combination is the seed that makes every other count come out right.
`test_combinations_are_unordered` is the one that catches an ordering bug: `4` from `{1, 2}` is
`1+1+1+1`, `1+1+2`, and `2+2`, which is three, not the larger number you'd get if you counted
orderings.

### Try to run the test

Nothing to import yet:

```
ModuleNotFoundError: No module named 'dp_knapsack.solutions.coin_change_ii'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub `change` to return `0` so the tests run:

```python
from __future__ import annotations

from collections.abc import Sequence


def change(amount: int, coins: Sequence[int]) -> int:
    return 0
```

Run `uv run pytest`:

```
    def test_classic_example():
>       assert change(5, [1, 2, 5]) == 4
E       assert 0 == 4
E        +  where 0 = change(5, [1, 2, 5])
```

Failing on the value. The two tests that expect `0` (`test_no_way_to_make_amount` and
`test_single_coin_does_not_divide`) pass by luck, which is the usual reminder that one green
test on its own proves nothing.

### Write enough code to make it pass

Build a `ways` table of length `amount + 1`, seed `ways[0] = 1` (one way to make nothing: take
no coins), then for each coin sweep the budget **upward**, adding in the combinations that end
by using this coin.

```python
from __future__ import annotations

from collections.abc import Sequence


def change(amount: int, coins: Sequence[int]) -> int:
    ways = [0] * (amount + 1)
    ways[0] = 1

    for coin in coins:
        for a in range(coin, amount + 1):
            ways[a] += ways[a - coin]

    return ways[amount]
```

The tests pass.

Now the part worth slowing down for: why does the coin loop sit *outside* the amount loop? Because
that's what makes combinations unordered. We finish considering coin `1` entirely before we ever
touch coin `2`, so every combination is built in a fixed coin order and counted exactly once. Swap
the loops (amount outside, coin inside) and you'd count `1+2` and `2+1` separately, which answers
a different question (the number of ordered sequences, a related problem people often confuse with
this one).

And the upward sweep is the unbounded half. When we read `ways[a - coin]`, it may already include
this same coin, so `{2, 2}` gets counted: that's exactly the reuse we want.

### Refactor

This is `knapsack_unbounded` with `take(current, prev)` as `current + prev` and a base table of
`[1, 0, 0, ...]`. Same upward sweep, same one-line update. No code change to make, but say the
mapping out loud so the next coin-counting problem feels like a re-skin rather than a new puzzle.
Re-run the tests.

## Problem 3: Target Sum

> Given an array `nums` and a `target`, count the ways to put a `+` or `-` in front of each
> number so the whole expression equals `target`.

This one doesn't look like knapsack at first. There's no budget and no "items under a cap", just
signs. The move is to turn it into a subset sum with a bit of algebra, and then it's Problem 1
wearing a hat (counting subsets instead of testing one).

Split the numbers into the ones we make positive (call their sum `P`) and the ones we make
negative (sum `N`). Then `P - N == target` and `P + N == total`. Add those two equations and the
`N` cancels: `2P == target + total`, so `P == (target + total) / 2`. So the question is just "how
many subsets sum to `P`", which is a 0/1 count knapsack: downward sweep, `take` is addition.

### Write the test first

```python
from .target_sum import find_target_sum_ways


def test_classic_example():
    assert find_target_sum_ways([1, 1, 1, 1, 1], 3) == 5


def test_single_number_hits_target():
    assert find_target_sum_ways([1], 1) == 1


def test_target_out_of_reach():
    assert find_target_sum_ways([1, 2], 5) == 0


def test_zero_can_take_either_sign():
    # The 0 contributes a +0 or a -0, doubling every way to reach the target.
    assert find_target_sum_ways([0, 1], 1) == 2


def test_negative_target_is_symmetric():
    assert find_target_sum_ways([1, 1, 1, 1, 1], -3) == 5


def test_impossible_parity():
    # sum is 1, target 0: (0 + 1) is odd, so no subset split exists.
    assert find_target_sum_ways([1], 0) == 0
```

`test_zero_can_take_either_sign` is the case that breaks naive solutions: a `0` can be `+0` or
`-0`, so it doubles the count without changing any sum. `test_impossible_parity` guards the
algebra: if `target + total` is odd, `P` isn't a whole number, so the answer is zero before we
build any table.

### Try to run the test

Nothing to import yet:

```
ModuleNotFoundError: No module named 'dp_knapsack.solutions.target_sum'
```

### Write the minimal amount of code for the test to run and check the failing test output

Stub it to return `0`:

```python
from __future__ import annotations

from collections.abc import Sequence


def find_target_sum_ways(nums: Sequence[int], target: int) -> int:
    return 0
```

Run `uv run pytest`:

```
    def test_classic_example():
>       assert find_target_sum_ways([1, 1, 1, 1, 1], 3) == 5
E       assert 0 == 5
E        +  where 0 = find_target_sum_ways([1, 1, 1, 1, 1], 3)
```

Four fail on the value, the two that expect `0` pass for the wrong reason. Now let's make them
all pass for the right one.

### Write enough code to make it pass

Do the algebra first: `needed = target + total`. If that's negative or odd, there's no valid
subset, so return `0`. Otherwise count subsets that sum to `needed // 2` with a downward sweep,
exactly like Problem 1 but accumulating counts instead of a boolean.

```python
from __future__ import annotations

from collections.abc import Sequence


def find_target_sum_ways(nums: Sequence[int], target: int) -> int:
    total = sum(nums)
    needed = target + total
    if needed < 0 or needed % 2 != 0:
        return 0

    subset_target = needed // 2
    ways = [0] * (subset_target + 1)
    ways[0] = 1

    for num in nums:
        for s in range(subset_target, num - 1, -1):
            ways[s] += ways[s - num]

    return ways[subset_target]
```

Green.

The zero case falls out for free, and it's a nice check on the sweep. With `num == 0`, the inner
range runs down to and including `s == 0`, so `ways[0] += ways[0]` doubles the seed. Every later
count reads from that doubled base, so a single `0` doubles the whole answer, which is precisely
`test_zero_can_take_either_sign` (`+0` and `-0` are two distinct ways).

### Refactor

The counting half is character-for-character the inner loop from Problem 1, with `+=` where we
had `or`. The only new idea was the algebra that reshaped a sign-assignment question into a subset
sum. **When a problem mentions choosing signs, or splitting into two groups with a sum
relationship, try the `P + N` / `P - N` substitution before reaching for anything fancier.** It
turns a scary-looking problem into one you've already solved. Re-run the tests.

## Wrapping up

- **Knapsack fills a 1D table indexed by a budget, deciding skip-or-take for one item at a
  time.** One outer pass over items, one inner pass over budgets.
- **Sweep direction is the whole pattern: down for 0/1 (each item once), up for unbounded (reuse
  allowed).** Getting that backwards is the signature knapsack bug.
- **`take` swaps to fit the question**: `or` for reachability (subset sum), `+` for counting
  combinations (coin change, target sum), `max` for best value.
- **Loop order controls ordered vs unordered counts.** Item loop outside, budget loop inside,
  and combinations stay unordered.
- **Reshape before you reach.** Equal partition is "hit `total / 2`", and target sum is a subset
  sum after the `P + N` algebra. The hard part is often spotting the knapsack, not coding it.

Next: [DP: Intervals](dp-intervals.md), where the table is indexed by a range rather than a
budget, and each cell is built from smaller ranges inside it.
