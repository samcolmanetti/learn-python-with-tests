from .coin_change_ii import change


def test_classic_example():
    assert change(5, [1, 2, 5]) == 4


def test_no_way_to_make_amount():
    assert change(3, [2]) == 0


def test_amount_zero_has_one_way():
    assert change(0, [1, 2, 5]) == 1


def test_no_coins_and_positive_amount():
    assert change(7, []) == 0


def test_single_coin_divides_evenly():
    assert change(10, [5]) == 1


def test_single_coin_does_not_divide():
    assert change(7, [5]) == 0


def test_combinations_are_unordered():
    # {2, 1, 1} and {1, 1, 2} are the same combination, counted once.
    assert change(4, [1, 2]) == 3
