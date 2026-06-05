from .number_of_islands import num_islands


def test_single_island():
    grid = [
        list("11110"),
        list("11010"),
        list("11000"),
        list("00000"),
    ]
    assert num_islands(grid) == 1


def test_three_islands():
    grid = [
        list("11000"),
        list("11000"),
        list("00100"),
        list("00011"),
    ]
    assert num_islands(grid) == 3


def test_diagonal_does_not_connect():
    grid = [
        list("10"),
        list("01"),
    ]
    assert num_islands(grid) == 2


def test_all_water():
    grid = [list("000"), list("000")]
    assert num_islands(grid) == 0


def test_empty_grid():
    assert num_islands([]) == 0
