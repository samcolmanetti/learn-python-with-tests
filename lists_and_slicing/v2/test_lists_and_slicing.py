from .lists_and_slicing import reversed_list, tail, total


def test_sums_a_list_of_numbers():
    assert total([1, 2, 3, 4, 5]) == 15


def test_sum_of_empty_list_is_zero():
    assert total([]) == 0


def test_reverses_a_list_via_slicing():
    assert reversed_list([1, 2, 3]) == [3, 2, 1]


def test_tail_drops_the_first_element():
    assert tail([1, 2, 3]) == [2, 3]


def test_tail_of_empty_list_is_empty():
    # Slicing tolerates out-of-range bounds instead of raising — unlike indexing.
    assert tail([]) == []
