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
