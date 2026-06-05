from .max_area_of_island import max_area_of_island


def test_largest_of_several_islands():
    grid = [
        [1, 1, 0, 0, 0],
        [1, 0, 0, 1, 1],
        [0, 0, 0, 1, 1],
        [0, 1, 0, 0, 0],
    ]
    assert max_area_of_island(grid) == 4


def test_single_island():
    grid = [
        [1, 1, 1],
        [0, 1, 0],
    ]
    assert max_area_of_island(grid) == 4


def test_all_water():
    grid = [
        [0, 0],
        [0, 0],
    ]
    assert max_area_of_island(grid) == 0


def test_diagonal_islands_counted_separately():
    grid = [
        [1, 0],
        [0, 1],
    ]
    assert max_area_of_island(grid) == 1


def test_empty_grid():
    assert max_area_of_island([]) == 0
