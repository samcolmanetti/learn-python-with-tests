from __future__ import annotations

from .course_schedule_ii import find_order


def _is_valid_order(num_courses: int, prerequisites: list[list[int]], order: list[int]) -> bool:
    if len(order) != num_courses or set(order) != set(range(num_courses)):
        return False
    position = {course: i for i, course in enumerate(order)}
    for course, needs in prerequisites:
        if position[needs] >= position[course]:
            return False
    return True


def test_no_prerequisites_lists_every_course():
    order = find_order(2, [])
    assert _is_valid_order(2, [], order)


def test_simple_chain():
    assert find_order(2, [[1, 0]]) == [0, 1]


def test_diamond_orders_prerequisites_first():
    prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]
    order = find_order(4, prerequisites)
    assert _is_valid_order(4, prerequisites, order)


def test_cycle_returns_empty():
    assert find_order(2, [[1, 0], [0, 1]]) == []


def test_single_course():
    assert find_order(1, []) == [0]
