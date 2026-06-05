from .daily_temperatures import daily_temperatures


def test_typical_run():
    assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]


def test_strictly_increasing():
    assert daily_temperatures([30, 40, 50, 60]) == [1, 1, 1, 0]


def test_strictly_decreasing():
    assert daily_temperatures([60, 50, 40, 30]) == [0, 0, 0, 0]


def test_equal_temperatures_never_count():
    assert daily_temperatures([50, 50, 50]) == [0, 0, 0]


def test_single_day():
    assert daily_temperatures([42]) == [0]


def test_empty():
    assert daily_temperatures([]) == []
