from .._template import build_list, to_list
from .merge_two_sorted import merge_two_sorted


def test_interleaves_two_lists():
    merged = merge_two_sorted(build_list([1, 2, 4]), build_list([1, 3, 4]))
    assert to_list(merged) == [1, 1, 2, 3, 4, 4]


def test_one_list_empty():
    assert to_list(merge_two_sorted(build_list([]), build_list([0]))) == [0]


def test_both_lists_empty():
    assert merge_two_sorted(build_list([]), build_list([])) is None


def test_one_list_runs_out_first():
    merged = merge_two_sorted(build_list([1, 2]), build_list([3, 4, 5]))
    assert to_list(merged) == [1, 2, 3, 4, 5]
