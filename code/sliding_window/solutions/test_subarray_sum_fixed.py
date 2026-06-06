import pytest

from .subarray_sum_fixed import max_subarray_sum


def test_basic_window():
    assert max_subarray_sum([1, 4, 2, 10, 2, 3], 3) == 16  # [4, 2, 10]


def test_window_equals_length():
    assert max_subarray_sum([1, 2, 3], 3) == 6


def test_single_element_windows():
    assert max_subarray_sum([5, -1, 3], 1) == 5


def test_handles_negatives():
    assert max_subarray_sum([-1, -2, -3, -4], 2) == -3  # [-1, -2]


@pytest.mark.parametrize("bad_k", [0, -1, 5])
def test_invalid_window_size_raises(bad_k):
    with pytest.raises(ValueError):
        max_subarray_sum([1, 2, 3], bad_k)
