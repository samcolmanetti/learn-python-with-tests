from .range_sum_query_immutable import NumArray


def test_basic_range():
    arr = NumArray([-2, 0, 3, -5, 2, -1])
    assert arr.sum_range(0, 2) == 1


def test_full_array():
    arr = NumArray([-2, 0, 3, -5, 2, -1])
    assert arr.sum_range(0, 5) == -3


def test_single_element():
    arr = NumArray([-2, 0, 3, -5, 2, -1])
    assert arr.sum_range(3, 3) == -5


def test_repeated_queries():
    arr = NumArray([-2, 0, 3, -5, 2, -1])
    assert arr.sum_range(2, 5) == -1
    assert arr.sum_range(0, 2) == 1
    assert arr.sum_range(1, 4) == 0
