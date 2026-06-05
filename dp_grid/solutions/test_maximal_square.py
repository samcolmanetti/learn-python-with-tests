from .maximal_square import maximal_square


def test_classic():
    matrix = [
        ["1", "0", "1", "0", "0"],
        ["1", "0", "1", "1", "1"],
        ["1", "1", "1", "1", "1"],
        ["1", "0", "0", "1", "0"],
    ]
    assert maximal_square(matrix) == 4


def test_single_one():
    assert maximal_square([["0", "1"]]) == 1


def test_all_zeros():
    assert maximal_square([["0", "0"], ["0", "0"]]) == 0


def test_full_square():
    assert maximal_square([["1", "1"], ["1", "1"]]) == 4


def test_single_zero_cell():
    assert maximal_square([["0"]]) == 0


def test_empty():
    assert maximal_square([]) == 0
