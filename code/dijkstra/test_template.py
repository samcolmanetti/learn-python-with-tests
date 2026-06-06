from ._template import dijkstra


def test_single_node():
    assert dijkstra({"a": []}, "a") == {"a": 0}


def test_straight_line():
    graph = {"a": [("b", 1)], "b": [("c", 2)], "c": []}
    assert dijkstra(graph, "a") == {"a": 0, "b": 1, "c": 3}


def test_prefers_cheaper_two_hop_path():
    # a -> b costs 5 directly, but a -> c -> b costs 1 + 1 = 2.
    graph = {
        "a": [("b", 5), ("c", 1)],
        "c": [("b", 1)],
        "b": [],
    }
    assert dijkstra(graph, "a") == {"a": 0, "c": 1, "b": 2}


def test_unreachable_node_is_absent():
    graph = {"a": [("b", 1)], "b": [], "island": []}
    result = dijkstra(graph, "a")
    assert "island" not in result


def test_zero_weight_edges():
    graph = {"a": [("b", 0)], "b": [("c", 0)], "c": []}
    assert dijkstra(graph, "a") == {"a": 0, "b": 0, "c": 0}
