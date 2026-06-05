from ._template import permutations, subsets


def test_subsets_of_empty():
    assert subsets([]) == [[]]


def test_subsets_power_set():
    result = subsets([1, 2, 3])
    expected = [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
    assert sorted(result) == sorted(expected)
    assert len(result) == 8


def test_permutations_of_empty():
    assert permutations([]) == [[]]


def test_permutations_count():
    result = permutations([1, 2, 3])
    expected = [
        [1, 2, 3],
        [1, 3, 2],
        [2, 1, 3],
        [2, 3, 1],
        [3, 1, 2],
        [3, 2, 1],
    ]
    assert sorted(result) == sorted(expected)
    assert len(result) == 6
