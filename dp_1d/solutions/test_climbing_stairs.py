from .climbing_stairs import climb_stairs


def test_zero_steps():
    assert climb_stairs(0) == 1


def test_one_step():
    assert climb_stairs(1) == 1


def test_two_steps():
    assert climb_stairs(2) == 2


def test_three_steps():
    assert climb_stairs(3) == 3


def test_five_steps():
    assert climb_stairs(5) == 8


def test_larger_input():
    assert climb_stairs(45) == 1836311903
