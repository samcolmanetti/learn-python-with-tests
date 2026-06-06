import bisect

import pytest
from hypothesis import given
from hypothesis import strategies as st

from .first_not_smaller import first_not_smaller


@pytest.mark.parametrize(
    ("arr", "target", "expected"),
    [
        ([1, 3, 3, 5, 8, 8, 10], 5, 3),
        ([1, 3, 3, 5, 8, 8, 10], 3, 1),  # first of the duplicates
        ([1, 3, 3, 5, 8, 8, 10], 0, 0),  # smaller than everything
        ([1, 3, 3, 5, 8, 8, 10], 11, 7),  # larger than everything -> len(arr)
        ([], 5, 0),  # empty array
        ([2], 2, 0),  # single element, equal
        ([2], 3, 1),  # single element, target larger
    ],
)
def test_first_not_smaller(arr, target, expected):
    assert first_not_smaller(arr, target) == expected


@given(
    st.lists(st.integers(), max_size=50).map(sorted),
    st.integers(),
)
def test_matches_bisect_left(arr, target):
    # Property: our hand-written boundary search must agree with the standard library.
    assert first_not_smaller(arr, target) == bisect.bisect_left(arr, target)
