import pytest

from .search_rotated import search


@pytest.mark.parametrize(
    ("nums", "target", "expected"),
    [
        ([4, 5, 6, 7, 0, 1, 2], 0, 4),
        ([4, 5, 6, 7, 0, 1, 2], 3, -1),
        ([4, 5, 6, 7, 0, 1, 2], 4, 0),  # pivot element
        ([4, 5, 6, 7, 0, 1, 2], 2, 6),  # last element
        ([1], 1, 0),
        ([1], 0, -1),
        ([], 5, -1),  # empty
        ([5, 1, 3], 3, 2),  # small rotation
    ],
)
def test_search_rotated(nums, target, expected):
    assert search(nums, target) == expected


def test_agrees_with_linear_scan_on_a_rotation():
    # Cross-check against the obvious O(n) implementation for every target in the array.
    base = [10, 20, 30, 40, 50]
    rotated = [30, 40, 50, 10, 20]
    for value in base:
        assert search(rotated, value) == rotated.index(value)
