from .house_robber import rob


def test_empty():
    assert rob([]) == 0


def test_single_house():
    assert rob([5]) == 5


def test_two_houses_take_larger():
    assert rob([2, 7]) == 7


def test_skip_middle():
    assert rob([1, 2, 3, 1]) == 4


def test_alternating_big():
    assert rob([2, 7, 9, 3, 1]) == 12


def test_all_equal():
    assert rob([4, 4, 4, 4]) == 8
