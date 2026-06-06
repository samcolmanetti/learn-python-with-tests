"""Dijkstra - shortest paths in a weighted graph with non-negative edges.

The graph is an adjacency dict mapping each node to a list of ``(neighbor, weight)`` pairs,
where every ``weight`` is ``>= 0``. ``dijkstra(graph, start)`` returns a dict mapping every
reachable node to the cost of the cheapest path from ``start``.

The engine is a min-heap of ``(distance, node)`` tuples. We always expand the closest
unsettled node next; because edges are non-negative, the first time we pop a node its distance
is final. Settle it once, relax its edges, never look at it again.
"""

from __future__ import annotations

import heapq
from collections.abc import Hashable, Mapping, Sequence


def dijkstra(
    graph: Mapping[Hashable, Sequence[tuple[Hashable, float]]],
    start: Hashable,
) -> dict[Hashable, float]:
    """Return the cheapest distance from ``start`` to every reachable node."""
    dist: dict[Hashable, float] = {start: 0}
    heap: list[tuple[float, Hashable]] = [(0, start)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue
        for neighbor, weight in graph.get(node, ()):
            candidate = d + weight
            if candidate < dist.get(neighbor, float("inf")):
                dist[neighbor] = candidate
                heapq.heappush(heap, (candidate, neighbor))
    return dist
