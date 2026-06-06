from .two_sum_sorted import two_sum


def test_finds_the_pair():
    assert two_sum([2, 7, 11, 15], 9) == (0, 1)


def test_pair_in_the_middle():
    assert two_sum([2, 3, 4], 6) == (0, 2)


def test_walks_inward_past_the_ends():
    # target 5: the ends (-3, 10) overshoot, so both pointers walk inward to 1 + 4.
    assert two_sum([-3, 0, 1, 4, 10], 5) == (2, 3)


def test_no_solution_returns_none():
    assert two_sum([1, 2, 3], 100) is None


def test_empty_returns_none():
    assert two_sum([], 0) is None
