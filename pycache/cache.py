from threading import Lock
from typing import Any

from .strategies import EvictionStrategy

_MISSING = object()

class Cache:
    def __init__(self, strategy: type[EvictionStrategy], capacity: int):
        self._strategy = strategy()
        self._capacity = capacity
        # Python dictionaries are insertion ordered and have O(1) time complexity on `get`, `set`, `del` and `in` since python 3.7
        self._cache = {}
        self._lock = Lock()

    def _get(self, key: str) -> Any:
        if key not in self._cache:
            return _MISSING
        self._strategy.access(key)
        return self._cache[key]

    def _set(self, key: str, value: Any):
        if key in self._cache:
            self._cache[key] = value
            self._strategy.access(key)
        else:
            if len(self._cache) >= self._capacity:
                evicted_key = self._strategy.evict()
                del self._cache[evicted_key]
            self._cache[key] = value
            self._strategy.add(key)

    def _delete(self, key: str):
        if key in self._cache:
            del self._cache[key]
            self._strategy.remove(key)

    def get(self, key) -> Any:
        """
        Gets the value associated with the given key from the cache.
        Args:
            key (str): The key to be retrieved from the cache.
        Returns:
            Any: The value associated with the key if it exists in the cache, otherwise None.
        """
        with self._lock:
            result = self._get(key)
            if result is _MISSING:
                return None
            return result


    def set(self, key: str, value: Any):
        """
        Sets a key-value pair in the cache. If the key already exists, the value will be updated. If the cache exceeds its capacity, the set eviction strategy will be applied to remove an existing key before adding the new key-value pair.
        Args:
            key (str): The key to be set in the cache.
            value (Any): The value to be associated with the key in the cache.
        """
        with self._lock:
            self._set(key, value)

    def delete(self, key: str):
        """
        Deletes a key from the cache if it exists and updates the eviction strategy accordingly.
        Args:
            key (str): The key to be deleted.
        """
        with self._lock:
            self._delete(key)


    def clear(self):
        """
        Clears all elements in the cache.
        """
        with self._lock:
            self._cache.clear()
            self._strategy = self._strategy.__class__()  # Reset strategy object

    # Allows checking the number of items in the cache with len()
    def __len__(self):
        with self._lock:
            return len(self._cache)

    # Allows checking if a key is in the cache with the 'in' keyword
    def __contains__(self, key):
        with self._lock:
            return key in self._cache

    # Allows iterations with the for loop
    def __iter__(self):
        with self._lock:
            items = list(self._cache.items()) # Create a snapshot of the current items to avoid a blocked thread-lock during iteration
        for key, value in items:
            yield key, value

    # Allows getting items with the [] operator, e.g. cache[key]
    def __getitem__(self, key) -> Any:
        with self._lock:
            result = self._get(key)
            if result is _MISSING:
                raise KeyError(key)
            return result

    # Allows setting items with the [] operator, e.g. cache[key] = value
    def __setitem__(self, key, value):
        with self._lock:
            self._set(key, value)

    # This allows deleting items with the `del` keyword, e.g. del cache[key]
    def __delitem__(self, key):
        with self._lock:
            self._delete(key)


    def memoize(self):
        """
        Decorator that caches function results.
        Usage:
            cache = Cache(LRUStrategy, capacity=100)

            @cache.memoize()
            def expensive_function(x,y):
                return x ** y
        :return:
        """

        def decorator(func):
            def wrapper(*args, **kwargs):
                key = f"{func.__name__}:{args}:{kwargs}"
                with self._lock:
                    result = self._get(key)
                if result is not _MISSING:
                    return result
                result = func(*args, **kwargs)
                with self._lock:
                    self._set(key, result)
                return result
            return wrapper
        return decorator