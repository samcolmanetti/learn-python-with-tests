from .coin_change import coin_change


def test_simple_combination():
    assert coin_change([1, 2, 5], 11) == 3


def test_impossible():
    assert coin_change([2], 3) == -1


def test_zero_amount():
    assert coin_change([1], 0) == 0


def test_exact_single_coin():
    assert coin_change([1, 2, 5], 5) == 1


def test_prefers_fewer_coins():
    assert coin_change([1, 3, 4], 6) == 2


def test_no_coins_nonzero_amount():
    assert coin_change([], 7) == -1
