import pytest

from pycache import Cache
from pycache.strategies import FIFOStrategy

@pytest.fixture
def example_cache():
    return Cache(strategy=FIFOStrategy, capacity=3)

@pytest.fixture
def big_example_cache():
    return Cache(strategy=FIFOStrategy, capacity=1000)

def test_cache_set_get(example_cache):
    example_cache.set("key1", "value1")
    example_cache.set("key2", "value2")

    assert example_cache.get("key1") == "value1"
    assert example_cache.get("key2") == "value2"

    example_cache["key3"] = "value3"
    assert example_cache["key3"] == "value3"

    example_cache.set("key1", "new_value1")
    assert example_cache.get("key1") == "new_value1"

def test_cache_delete(example_cache):
    example_cache.set("key5", "value5")
    example_cache.set("key6", "value6")

    example_cache.delete("key5")
    assert example_cache.get("key5") is None

    with pytest.raises(KeyError):
        _ = example_cache["nonexistent"]

    del example_cache["key6"]
    assert example_cache.get("key6") is None

    example_cache.delete("nonexistent") # Should not raise an error

def test_cache_len(example_cache):
    assert len(example_cache) == 0
    example_cache.set("key1", "value1")
    example_cache.set("key2", "value2")
    assert len(example_cache) == 2
    example_cache.delete("key1")
    assert len(example_cache) == 1

def test_cache_clear(example_cache):
    example_cache.set("key7", "value7")
    example_cache.set("key8", "value8")
    assert len(example_cache) == 2
    example_cache.clear()
    assert len(example_cache) == 0

def test_cache_in_operator(example_cache):
    example_cache.set("key9", "value9")
    assert "key9" in example_cache
    assert "nonexistent" not in example_cache

def test_cache_iteration(example_cache):
    example_cache.set("key10", "value10")
    example_cache.set("key11", "value11")
    example_cache.set("key12", "value12")

    for key, value in example_cache:
        assert (key, value) in [("key10", "value10"), ("key11", "value11"), ("key12", "value12")]

def test_cache_eviction(example_cache):
    example_cache.set("key13", "value13")
    example_cache.set("key14", "value14")
    example_cache.set("key15", "value15")
    example_cache.set("key16", "value16")

    assert example_cache.get("key13") is None
    assert example_cache.get("key14") == "value14"
    assert example_cache.get("key15") == "value15"
    assert example_cache.get("key16") == "value16"

def test_cache_thread_safe(big_example_cache):
    import threading, time

    def worker(id):
        for i in range(100):
            big_example_cache.set(f"thread{id}_key{i}", f"value{i}")
            time.sleep(0.0001) # Simulate an input/output operation

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    for i in range(5):
        for j in range(100):
            print(f"Checking thread{i}_key{j}")
            assert big_example_cache.get(f"thread{i}_key{j}") == f"value{j}"

def test_cache_memoization(big_example_cache):
    calls = 0

    @big_example_cache.memoize()
    def fibonacci(n):
        nonlocal calls
        calls += 1
        if n <= 1:
            return n
        return fibonacci(n-1) + fibonacci(n-2)

    call1 = fibonacci(35)
    first_calls = calls
    call2 = fibonacci(35)
    second_calls = calls
    call3 = fibonacci(36)
    third_calls = calls

    assert call1 == call2 == 9227465
    assert first_calls > 1
    assert first_calls == second_calls
    assert call3 == 14930352
    assert second_calls != third_calls

def test_cache_edge_cases():
    with pytest.raises(ValueError):
        cache = Cache(strategy=FIFOStrategy, capacity=0)