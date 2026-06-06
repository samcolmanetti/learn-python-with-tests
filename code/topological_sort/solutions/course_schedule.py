from __future__ import annotations

from collections import deque


def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    """Can every course be taken given the prerequisite pairs?

    Each pair ``[course, needs]`` means you must take ``needs`` before ``course``.
    You can finish exactly when the prerequisite graph has no cycle.
    """
    graph: dict[int, list[int]] = {course: [] for course in range(num_courses)}
    indegree = [0] * num_courses
    for course, needs in prerequisites:
        graph[needs].append(course)
        indegree[course] += 1

    queue = deque(course for course in range(num_courses) if indegree[course] == 0)
    taken = 0
    while queue:
        course = queue.popleft()
        taken += 1
        for nxt in graph[course]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    return taken == num_courses
