from .remove_duplicates import remove_duplicates


def test_removes_duplicates_in_place():
    nums = [1, 1, 2, 2, 3]
    k = remove_duplicates(nums)
    assert k == 3
    assert nums[:k] == [1, 2, 3]


def test_no_duplicates_unchanged():
    nums = [1, 2, 3]
    assert remove_duplicates(nums) == 3
    assert nums == [1, 2, 3]


def test_all_same():
    nums = [7, 7, 7, 7]
    k = remove_duplicates(nums)
    assert k == 1
    assert nums[:k] == [7]


def test_empty():
    assert remove_duplicates([]) == 0


def test_single():
    nums = [5]
    assert remove_duplicates(nums) == 1
    assert nums[:1] == [5]
