from .insert_interval import insert


def test_insert_into_gap():
    assert insert([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]


def test_insert_overlapping_several():
    assert insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == [
        [1, 2],
        [3, 10],
        [12, 16],
    ]


def test_insert_into_empty():
    assert insert([], [5, 7]) == [[5, 7]]


def test_insert_before_everything():
    assert insert([[3, 5], [8, 10]], [1, 2]) == [[1, 2], [3, 5], [8, 10]]


def test_insert_after_everything():
    assert insert([[1, 2], [3, 5]], [8, 10]) == [[1, 2], [3, 5], [8, 10]]


def test_insert_touching_neighbours_merges_them():
    assert insert([[1, 2], [5, 6]], [2, 5]) == [[1, 6]]
