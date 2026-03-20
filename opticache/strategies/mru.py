from collections import OrderedDict
from typing import Any

from .base import EvictionStrategy


class MRUStrategy(EvictionStrategy):
    """
    MRU (Most Recently Used) eviction strategy implementation.
    This strategy evicts the most recently accessed key
    when the cache exceeds its capacity.
    """
    def __init__(self):
        # OrderedDict has O(1) time complexity
        self._order = OrderedDict()

    def add(self, key):
        self._order[key] = None

    def access(self, key):
        self._order.move_to_end(key)

    def evict(self) -> Any:
        if not self._order:
            raise IndexError("No keys to evict")
        return self._order.popitem(last=True)[0]

    def remove(self, key):
        del self._order[key]
