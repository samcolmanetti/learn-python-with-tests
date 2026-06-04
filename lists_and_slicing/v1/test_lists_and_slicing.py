from .lists_and_slicing import total


def test_sums_a_list_of_numbers():
    assert total([1, 2, 3, 4, 5]) == 15
