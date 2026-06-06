from __future__ import annotations

from .course_schedule import can_finish


def test_no_prerequisites():
    assert can_finish(2, []) is True


def test_simple_chain():
    assert can_finish(2, [[1, 0]]) is True


def test_direct_cycle():
    assert can_finish(2, [[1, 0], [0, 1]]) is False


def test_longer_cycle():
    assert can_finish(3, [[1, 0], [2, 1], [0, 2]]) is False


def test_diamond_is_fine():
    assert can_finish(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) is True


def test_self_loop_is_a_cycle():
    assert can_finish(1, [[0, 0]]) is False
