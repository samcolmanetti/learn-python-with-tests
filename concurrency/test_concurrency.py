import asyncio

from .concurrency import (
    fetch_all,
    fetch_value,
    gather_values,
    parallel_map,
    square,
)


def test_square():
    assert square(5) == 25


def test_parallel_map_preserves_order():
    assert parallel_map([1, 2, 3, 4]) == [1, 4, 9, 16]


def test_parallel_map_result_set():
    result = parallel_map([3, 1, 2])
    assert set(result) == {1, 4, 9}


def test_parallel_map_empty():
    assert parallel_map([]) == []


def test_parallel_map_single_worker_matches():
    assert parallel_map([2, 3, 4], workers=1) == [4, 9, 16]


def test_fetch_value_coroutine():
    assert asyncio.run(fetch_value(6)) == 36


def test_gather_values_preserves_order():
    assert asyncio.run(gather_values([1, 2, 3])) == [1, 4, 9]


def test_fetch_all():
    assert fetch_all([2, 3, 4]) == [4, 9, 16]


def test_fetch_all_empty():
    assert fetch_all([]) == []
