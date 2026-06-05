from .combination_sum import combination_sum


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
