from .next_greater_element_ii import next_greater_circular


def test_wraps_around():
    assert next_greater_circular([1, 2, 1]) == [2, -1, 2]


def test_all_equal_have_no_greater():
    assert next_greater_circular([5, 5, 5]) == [-1, -1, -1]


def test_descending_wraps_to_the_max():
    assert next_greater_circular([5, 4, 3, 2, 1]) == [-1, 5, 5, 5, 5]


def test_ascending():
    assert next_greater_circular([1, 2, 3, 4]) == [2, 3, 4, -1]


def test_single_element():
    assert next_greater_circular([7]) == [-1]


def test_duplicates_take_next_strictly_greater():
    assert next_greater_circular([1, 2, 3, 2, 1]) == [2, 3, -1, 3, 2]
