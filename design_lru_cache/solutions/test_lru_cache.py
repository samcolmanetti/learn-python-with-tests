from .lru_cache import LRUCache


def test_get_miss_returns_minus_one():
    cache = LRUCache(2)
    assert cache.get(1) == -1


def test_put_then_get_returns_value():
    cache = LRUCache(2)
    cache.put(1, 100)
    assert cache.get(1) == 100


def test_update_existing_key_overwrites_value():
    cache = LRUCache(2)
    cache.put(1, 100)
    cache.put(1, 200)
    assert cache.get(1) == 200


def test_eviction_drops_least_recently_used():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(3, 3)  # capacity is 2, so the oldest key (1) is evicted
    assert cache.get(1) == -1
    assert cache.get(2) == 2
    assert cache.get(3) == 3


def test_get_refreshes_recency():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.get(1)  # now 1 is most recently used, 2 is least
    cache.put(3, 3)  # evicts 2, not 1
    assert cache.get(2) == -1
    assert cache.get(1) == 1
    assert cache.get(3) == 3


def test_update_refreshes_recency():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(1, 10)  # updating 1 also makes it most recently used
    cache.put(3, 3)  # evicts 2
    assert cache.get(2) == -1
    assert cache.get(1) == 10
    assert cache.get(3) == 3


def test_capacity_one_keeps_only_latest():
    cache = LRUCache(1)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == -1
    assert cache.get(2) == 2
