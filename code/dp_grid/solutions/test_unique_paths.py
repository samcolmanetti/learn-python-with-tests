from .unique_paths import unique_paths


def test_three_by_seven():
    assert unique_paths(3, 7) == 28


def test_three_by_two():
    assert unique_paths(3, 2) == 3


def test_single_row():
    assert unique_paths(1, 5) == 1


def test_single_cell():
    assert unique_paths(1, 1) == 1


def test_square():
    assert unique_paths(4, 4) == 20


def test_empty_grid():
    assert unique_paths(0, 5) == 0
