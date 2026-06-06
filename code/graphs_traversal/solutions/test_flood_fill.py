from .flood_fill import flood_fill


def test_fills_connected_region():
    image = [
        [1, 1, 1],
        [1, 1, 0],
        [1, 0, 1],
    ]
    assert flood_fill(image, 1, 1, 2) == [
        [2, 2, 2],
        [2, 2, 0],
        [2, 0, 1],
    ]


def test_no_change_when_color_matches():
    image = [
        [0, 0, 0],
        [0, 1, 1],
    ]
    assert flood_fill(image, 1, 1, 1) == [
        [0, 0, 0],
        [0, 1, 1],
    ]


def test_single_pixel():
    image = [[5]]
    assert flood_fill(image, 0, 0, 9) == [[9]]


def test_diagonal_not_filled():
    image = [
        [1, 0],
        [0, 1],
    ]
    assert flood_fill(image, 0, 0, 7) == [
        [7, 0],
        [0, 1],
    ]
