from lists_and_slicing import copy_of, every_other, reversed_list, tail, total


def test_sums_a_list_of_numbers():
    assert total([1, 2, 3, 4, 5]) == 15


def test_sum_of_empty_list_is_zero():
    assert total([]) == 0


def test_reverses_a_list_via_slicing():
    assert reversed_list([1, 2, 3]) == [3, 2, 1]


def test_tail_handles_empty_and_nonempty():
    assert tail([1, 2, 3]) == [2, 3]
    assert tail([]) == []


def test_every_other_takes_a_step_slice():
    assert every_other([0, 1, 2, 3, 4, 5]) == [0, 2, 4]


def test_slicing_makes_a_copy_not_an_alias():
    original = [1, 2, 3]
    a_copy = copy_of(original)
    a_copy.append(4)
    # Mutating the copy must NOT touch the original.
    assert a_copy == [1, 2, 3, 4]
    assert original == [1, 2, 3]


def test_plain_assignment_is_an_alias():
    original = [1, 2, 3]
    alias = original  # NOT a copy, same underlying list object
    alias.append(4)
    assert original == [1, 2, 3, 4]
