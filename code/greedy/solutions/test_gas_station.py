from .gas_station import can_complete_circuit


def test_simple_circuit():
    gas = [1, 2, 3, 4, 5]
    cost = [3, 4, 5, 1, 2]
    assert can_complete_circuit(gas, cost) == 3


def test_impossible_circuit():
    gas = [2, 3, 4]
    cost = [3, 4, 3]
    assert can_complete_circuit(gas, cost) == -1


def test_single_station_enough():
    assert can_complete_circuit([5], [4]) == 0


def test_single_station_not_enough():
    assert can_complete_circuit([3], [4]) == -1


def test_start_at_zero():
    gas = [5, 1, 2, 3, 4]
    cost = [4, 4, 1, 5, 1]
    assert can_complete_circuit(gas, cost) == 4


def test_exact_balance():
    gas = [2, 2, 2]
    cost = [2, 2, 2]
    assert can_complete_circuit(gas, cost) == 0
