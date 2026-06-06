from .network_delay_time import network_delay_time


def test_reaches_all_nodes():
    times = [[2, 1, 1], [2, 3, 1], [3, 4, 1]]
    assert network_delay_time(times, 4, 2) == 2


def test_single_node_no_travel():
    assert network_delay_time([], 1, 1) == 0


def test_unreachable_node_returns_minus_one():
    times = [[1, 2, 1]]
    assert network_delay_time(times, 3, 1) == -1


def test_prefers_cheaper_two_hop_path():
    # 1 -> 2 directly costs 5, but 1 -> 3 -> 2 costs 1 + 1 = 2.
    times = [[1, 2, 5], [1, 3, 1], [3, 2, 1]]
    assert network_delay_time(times, 3, 1) == 2


def test_last_node_sets_the_time():
    times = [[1, 2, 1], [1, 3, 4]]
    assert network_delay_time(times, 3, 1) == 4
