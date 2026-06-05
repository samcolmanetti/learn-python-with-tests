from __future__ import annotations

import heapq


def network_delay_time(times: list[list[int]], n: int, source: int) -> int:
    """Return how long it takes a signal from ``source`` to reach all ``n`` nodes.

    ``times`` is a list of ``[u, v, w]`` directed edges; nodes are labelled ``1..n``.
    Return the time the last node receives the signal, or ``-1`` if some node never does.
    """
    graph: dict[int, list[tuple[int, int]]] = {}
    for u, v, w in times:
        graph.setdefault(u, []).append((v, w))

    dist: dict[int, int] = {source: 0}
    heap: list[tuple[int, int]] = [(0, source)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue
        for neighbor, weight in graph.get(node, ()):
            candidate = d + weight
            if candidate < dist.get(neighbor, float("inf")):
                dist[neighbor] = candidate
                heapq.heappush(heap, (candidate, neighbor))

    if len(dist) < n:
        return -1
    return max(dist.values())
