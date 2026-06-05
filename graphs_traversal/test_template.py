from ._template import bfs, dfs, grid_neighbors


def test_bfs_visits_in_breadth_order():
    graph = {
        "a": ["b", "c"],
        "b": ["d"],
        "c": ["d"],
        "d": [],
    }
    assert bfs(graph, "a") == ["a", "b", "c", "d"]


def test_bfs_handles_a_cycle():
    graph = {1: [2], 2: [3], 3: [1]}
    assert bfs(graph, 1) == [1, 2, 3]


def test_dfs_goes_deep_first():
    graph = {
        "a": ["b", "c"],
        "b": ["d"],
        "c": [],
        "d": [],
    }
    assert dfs(graph, "a") == ["a", "b", "d", "c"]


def test_dfs_handles_a_cycle():
    graph = {1: [2], 2: [3], 3: [1]}
    assert dfs(graph, 1) == [1, 2, 3]


def test_grid_neighbors_in_the_middle():
    grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    assert sorted(grid_neighbors(grid, 1, 1)) == [(0, 1), (1, 0), (1, 2), (2, 1)]


def test_grid_neighbors_clips_at_a_corner():
    grid = [[0, 0], [0, 0]]
    assert sorted(grid_neighbors(grid, 0, 0)) == [(0, 1), (1, 0)]
