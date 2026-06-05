from .min_cost_grid import min_cost_grid


def test_single_cell():
    assert min_cost_grid([[5]]) == 5


def test_empty_grid():
    assert min_cost_grid([]) == -1


def test_single_row():
    assert min_cost_grid([[1, 2, 3]]) == 6


def test_classic_min_path():
    assert min_cost_grid([[1, 3, 1], [1, 5, 1], [4, 2, 1]]) == 7


def test_detour_beats_straight_line():
    # A down-then-right DP is forced through a 100 cell. Dijkstra walks the cheap
    # left column and bottom row instead: 1+1+1 down, then 1+1 across = 5.
    grid = [
        [1, 100, 1],
        [1, 100, 1],
        [1, 1, 1],
    ]
    assert min_cost_grid(grid) == 5
