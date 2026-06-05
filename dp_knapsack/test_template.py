from ._template import knapsack_01, knapsack_unbounded


def test_01_picks_each_item_at_most_once():
    # Two items of cost 3; with 0/1 a budget of 6 can hold both, a budget of 5 only one.
    base = [0] * 7
    dp = knapsack_01([3, 3], 6, base, lambda current, candidate: max(current, candidate + 1))
    assert dp[6] == 2
    assert dp[5] == 1


def test_unbounded_reuses_one_item():
    # A single item of cost 2 can be taken three times into a budget of 6.
    base = [0] * 7
    dp = knapsack_unbounded([2], 6, base, lambda current, candidate: max(current, candidate + 1))
    assert dp[6] == 3
    assert dp[5] == 2


def test_unbounded_counts_ways_with_addition():
    # Counting combinations that sum to the budget: take(current, candidate) = current + candidate.
    base = [0] * 6
    base[0] = 1
    dp = knapsack_unbounded([1, 2, 5], 5, base, lambda current, candidate: current + candidate)
    assert dp[5] == 4
