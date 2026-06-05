"""Topological Sort, order a DAG so every edge points "forward" (Kahn's algorithm).

Compute each node's in-degree (number of prerequisites). Repeatedly take a node with
in-degree 0, append it to the order, and decrement its neighbours' in-degrees, enqueuing any
that reach 0. If you can't place every node, the graph has a **cycle**, there is no valid
ordering.

This doubles as cycle detection: ``topo_sort`` returns ``None`` when the graph is cyclic.

Graphs are ``dict[node, list[node]]`` adjacency lists (edge ``u -> v`` means "u before v").
"""

from __future__ import annotations

from collections import deque


def topo_sort(graph: dict) -> list | None:
    """A topological ordering of ``graph``, or ``None`` if it contains a cycle."""
    indegree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            # A neighbor that never appears as a key (a pure sink) still needs an entry.
            indegree[neighbor] = indegree.get(neighbor, 0) + 1

    queue = deque(node for node, deg in indegree.items() if deg == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, ()):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return order if len(order) == len(indegree) else None
