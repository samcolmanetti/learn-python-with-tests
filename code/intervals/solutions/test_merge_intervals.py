from .merge_intervals import merge


def test_overlapping_pair():
    assert merge([[1, 3], [2, 6]]) == [[1, 6]]


def test_touching_intervals_merge():
    assert merge([[1, 4], [4, 5]]) == [[1, 5]]


def test_disjoint_intervals_stay_separate():
    assert merge([[1, 2], [5, 6]]) == [[1, 2], [5, 6]]


def test_unsorted_input():
    assert merge([[2, 6], [1, 3], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]


def test_interval_swallowed_by_a_wider_one():
    assert merge([[1, 10], [2, 4], [5, 6]]) == [[1, 10]]


def test_empty():
    assert merge([]) == []
