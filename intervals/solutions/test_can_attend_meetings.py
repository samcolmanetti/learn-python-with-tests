from .can_attend_meetings import can_attend_meetings


def test_overlapping_meetings_cannot_all_be_attended():
    assert can_attend_meetings([[0, 30], [5, 10], [15, 20]]) is False


def test_disjoint_meetings_can_all_be_attended():
    assert can_attend_meetings([[7, 10], [2, 4]]) is True


def test_touching_meetings_are_fine():
    assert can_attend_meetings([[1, 5], [5, 8]]) is True


def test_no_meetings():
    assert can_attend_meetings([]) is True


def test_single_meeting():
    assert can_attend_meetings([[4, 9]]) is True
