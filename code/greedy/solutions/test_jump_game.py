from .jump_game import can_jump


def test_reachable():
    assert can_jump([2, 3, 1, 1, 4]) is True


def test_blocked_by_zero():
    assert can_jump([3, 2, 1, 0, 4]) is False


def test_single_element():
    assert can_jump([0]) is True


def test_leading_zero_with_more():
    assert can_jump([0, 1]) is False


def test_exact_jumps():
    assert can_jump([1, 1, 1, 1]) is True


def test_big_first_jump():
    assert can_jump([5, 0, 0, 0, 0]) is True
