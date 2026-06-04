from .product_of_array_except_self import product_except_self


def test_no_zeros():
    assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]


def test_one_zero():
    assert product_except_self([0, 4, 3]) == [12, 0, 0]


def test_two_zeros():
    assert product_except_self([0, 4, 0]) == [0, 0, 0]


def test_negatives():
    assert product_except_self([-1, 1, 2, -3]) == [-6, 6, 3, -2]
