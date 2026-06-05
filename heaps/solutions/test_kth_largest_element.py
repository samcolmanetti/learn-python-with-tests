from .kth_largest_element import find_kth_largest


def test_kth_largest_in_unsorted():
    assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5


def test_with_duplicates():
    assert find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4


def test_largest_is_first():
    assert find_kth_largest([7, 7, 7], 1) == 7


def test_kth_equals_length():
    assert find_kth_largest([3, 2, 1, 5, 6, 4], 6) == 1


def test_handles_negatives():
    assert find_kth_largest([-1, -5, -3, -2], 2) == -2
