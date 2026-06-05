from .top_k_frequent import top_k_frequent


def test_two_most_frequent():
    assert top_k_frequent([1, 1, 1, 2, 2, 3], 2) == [1, 2]


def test_single_element():
    assert top_k_frequent([1], 1) == [1]


def test_all_distinct_k_equals_length():
    assert sorted(top_k_frequent([5, 6, 7], 3)) == [5, 6, 7]


def test_most_frequent_first():
    assert top_k_frequent([4, 4, 4, 9, 9, 1], 1) == [4]


def test_handles_negatives():
    assert top_k_frequent([-1, -1, -2, -2, -2, 3], 2) == [-2, -1]
