from collections import deque
from typing import Any

from .base import EvictionStrategy


class FIFOStrategy(EvictionStrategy):
    """
    FIFO (First In First Out) eviction strategy implementation.
    This strategy evicts the key that was added first
    when the cache exceeds its capacity.
    If you expect to delete keys from the cache frequently
    in big data sets, consider using FIFOStrategyFastDelete
    which has O(1) time complexity for deletes.
    """
    def __init__(self):
        self._order = deque()

    def add(self, key):
        self._order.append(key)

    def access(self, key):
        pass  # Not used by FIFO

    def evict(self) -> Any:
        if not self._order:
            raise Exception("No keys to evict")
        return self._order.popleft()

    def remove(self, key):
        self._order.remove(key)
