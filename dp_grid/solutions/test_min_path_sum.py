from .min_path_sum import min_path_sum


def test_classic():
    grid = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
    assert min_path_sum(grid) == 7


def test_single_row():
    assert min_path_sum([[1, 2, 3]]) == 6


def test_single_column():
    assert min_path_sum([[1], [2], [3]]) == 6


def test_single_cell():
    assert min_path_sum([[5]]) == 5


def test_two_by_two():
    assert min_path_sum([[1, 2], [1, 1]]) == 3


def test_empty():
    assert min_path_sum([]) == 0
