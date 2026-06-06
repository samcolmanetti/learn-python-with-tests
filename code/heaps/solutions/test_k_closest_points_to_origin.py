from .k_closest_points_to_origin import k_closest


def sorted_points(points):
    return sorted(sorted(p) for p in points)


def test_single_closest():
    result = k_closest([[1, 3], [-2, 2]], 1)
    assert sorted_points(result) == [[-2, 2]]


def test_two_closest_ignores_order():
    result = k_closest([[3, 3], [5, -1], [-2, 4]], 2)
    assert sorted_points(result) == sorted_points([[3, 3], [-2, 4]])


def test_k_equals_length_returns_all():
    result = k_closest([[1, 1], [2, 2], [3, 3]], 3)
    assert sorted_points(result) == [[1, 1], [2, 2], [3, 3]]


def test_origin_point_is_closest():
    result = k_closest([[0, 0], [4, 4], [1, 0]], 2)
    assert sorted_points(result) == sorted_points([[0, 0], [1, 0]])


def test_ties_in_distance():
    result = k_closest([[1, 0], [0, 1], [2, 2]], 2)
    assert sorted_points(result) == sorted_points([[1, 0], [0, 1]])
