from __future__ import annotations

from ._template import topo_sort


def _is_valid_order(graph: dict, order: list) -> bool:
    position = {node: i for i, node in enumerate(order)}
    for node in graph:
        for neighbor in graph[node]:
            if position[node] >= position[neighbor]:
                return False
    return True


def test_linear_chain():
    graph = {"a": ["b"], "b": ["c"], "c": []}
    assert topo_sort(graph) == ["a", "b", "c"]


def test_every_edge_points_forward():
    graph = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}
    order = topo_sort(graph)
    assert order is not None
    assert _is_valid_order(graph, order)


def test_sink_not_listed_as_a_key():
    # "c" only ever appears as a neighbor, never as a key.
    graph = {"a": ["b"], "b": ["c"]}
    order = topo_sort(graph)
    assert order is not None
    assert set(order) == {"a", "b", "c"}
    assert _is_valid_order(graph, order)


def test_cycle_returns_none():
    assert topo_sort({"a": ["b"], "b": ["a"]}) is None


def test_empty_graph():
    assert topo_sort({}) == []
