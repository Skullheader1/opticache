from typing import Any

from .strategies import EvictionStrategy


class Cache:
    def __init__(self, strategy: type[EvictionStrategy], capacity: int):
        self._strategy = strategy()
        self._capacity = capacity
        # Python dictionaries are insertion ordered and have O(1) time complexity on `get`, `set`, `del` and `in` since python 3.7
        self._cache = {}


    def get(self, key):
        """
        Gets the value associated with the given key from the cache.
        Args:
            key (str): The key to be retrieved from the cache.
        Returns:
            Any: The value associated with the key if it exists in the cache, otherwise None.
        """
        if key not in self._cache:
            return None
        self._strategy.access(key)
        return self._cache[key]


    def set(self, key: str, value: Any):
        """
        Sets a key-value pair in the cache. If the key already exists, the value will be updated. If the cache exceeds its capacity, the set eviction strategy will be applied to remove an existing key before adding the new key-value pair.
        Args:
            key (str): The key to be set in the cache.
            value (Any): The value to be associated with the key in the cache.
        """
        if key in self._cache:
            self._cache[key] = value
            self._strategy.access(key)
        else:
            if len(self._cache) >= self._capacity:
                evicted_key = self._strategy.evict()
                del self._cache[evicted_key]
            self._cache[key] = value
            self._strategy.add(key)

    def delete(self, key: str):
        """
        Deletes a key from the cache if it exists and updates the eviction strategy accordingly.
        Args:
            key (str): The key to be deleted.
        """
        if key in self._cache:
            del self._cache[key]
            self._strategy.remove(key)


    def clear(self):
        """
        Clears all elements in the cache.
        """
        self._cache.clear()
        self._strategy = self._strategy.__class__()  # Reset strategy object

    # Allows checking the number of items in the cache with len()
    def __len__(self):
        return len(self._cache)

    # Allows checking if a key is in the cache with the 'in' keyword
    def __contains__(self, key):
        return key in self._cache

    # Allows iterations with the for loop
    def __iter__(self):
        for key in self._cache:
            yield key, self._cache[key]