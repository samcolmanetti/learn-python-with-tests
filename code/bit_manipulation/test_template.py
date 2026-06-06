from ._template import clear_lowest_set_bit, is_bit_set, lowest_set_bit


def test_lowest_set_bit_isolates_rightmost_one():
    assert lowest_set_bit(0b1100) == 0b0100


def test_lowest_set_bit_of_zero_is_zero():
    assert lowest_set_bit(0) == 0


def test_clear_lowest_set_bit_removes_rightmost_one():
    assert clear_lowest_set_bit(0b1100) == 0b1000


def test_is_bit_set_true_and_false():
    assert is_bit_set(0b1010, 1) is True
    assert is_bit_set(0b1010, 0) is False
