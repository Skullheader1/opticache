from opticache import Cache
from opticache.strategies import (FIFOStrategy,
                                  LRUStrategy,
                                  LFUStrategy,
                                  FIFOStrategyFastDelete,
                                  MRUStrategy,
                                  RandomStrategy,
                                  SIEVEStrategy)


def test_fifo_eviction():
    cache = Cache(strategy=FIFOStrategy, capacity=2)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")

    assert cache.get("key1") is None
    assert cache.get("key2") == "value2"
    assert cache.get("key3") == "value3"


def test_lru_eviction():
    cache = Cache(strategy=LRUStrategy, capacity=2)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.get("key1")
    cache.set("key3", "value3")

    assert cache.get("key1") == "value1"
    assert cache.get("key2") is None
    assert cache.get("key3") == "value3"


def test_lfu_eviction():
    cache = Cache(strategy=LFUStrategy, capacity=2)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.get("key1")
    cache.get("key1")
    cache.get("key2")
    cache.set("key3", "value3")

    assert cache.get("key1") == "value1"
    assert cache.get("key2") is None
    assert cache.get("key3") == "value3"


def test_fifo_fast_delete_eviction():
    cache = Cache(strategy=FIFOStrategyFastDelete, capacity=2)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")

    assert cache.get("key1") is None
    assert cache.get("key2") == "value2"
    assert cache.get("key3") == "value3"


def test_mru_eviction():
    cache = Cache(strategy=MRUStrategy, capacity=2)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.get("key1")
    cache.set("key3", "value3")

    assert cache.get("key1") is None
    assert cache.get("key2") == "value2"
    assert cache.get("key3") == "value3"


def test_random_eviction():
    cache = Cache(strategy=RandomStrategy, capacity=2)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")

    key1_exists = cache.get("key1") == "value1"
    key2_exists = cache.get("key2") == "value2"

    assert key1_exists or key2_exists
    assert not (key1_exists and key2_exists)
    assert cache.get("key3") == "value3"


def test_sieve_eviction():
    cache = Cache(strategy=SIEVEStrategy, capacity=3)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")

    cache.get("key1")
    cache.get("key3")

    cache.set("key4", "value4")

    assert cache.get("key1") == "value1"
    assert cache.get("key2") is None
    assert cache.get("key3") == "value3"
    assert cache.get("key4") == "value4"
