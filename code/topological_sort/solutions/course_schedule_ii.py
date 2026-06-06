from __future__ import annotations

from collections import deque


def find_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    """A valid order to take all courses, or ``[]`` if none exists.

    Each pair ``[course, needs]`` means ``needs`` must come before ``course``.
    Returns one topological ordering, or an empty list when the graph is cyclic.
    """
    graph: dict[int, list[int]] = {course: [] for course in range(num_courses)}
    indegree = [0] * num_courses
    for course, needs in prerequisites:
        graph[needs].append(course)
        indegree[course] += 1

    queue = deque(course for course in range(num_courses) if indegree[course] == 0)
    order: list[int] = []
    while queue:
        course = queue.popleft()
        order.append(course)
        for nxt in graph[course]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    return order if len(order) == num_courses else []
