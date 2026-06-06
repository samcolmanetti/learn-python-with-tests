from .subarray_sum_equals_k import subarray_sum


def test_repeated_ones():
    assert subarray_sum([1, 1, 1], 2) == 2


def test_distinct_values():
    assert subarray_sum([1, 2, 3], 3) == 2


def test_zero_target_with_negatives():
    assert subarray_sum([1, -1, 0], 0) == 3


def test_empty():
    assert subarray_sum([], 0) == 0


def test_single_element_hit():
    assert subarray_sum([5], 5) == 1


def test_single_element_miss():
    assert subarray_sum([5], 3) == 0
