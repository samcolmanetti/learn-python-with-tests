from .single_number import single_number


def test_single_in_the_middle():
    assert single_number([2, 2, 1]) == 1


def test_single_with_repeats_spread_out():
    assert single_number([4, 1, 2, 1, 2]) == 4


def test_only_one_element():
    assert single_number([7]) == 7


def test_zero_is_a_valid_answer():
    assert single_number([3, 0, 3]) == 0


def test_handles_negatives():
    assert single_number([-5, 9, 9]) == -5
