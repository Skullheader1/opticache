from collections import OrderedDict
from typing import Any

from .base import EvictionStrategy


class FIFOStrategyFastDelete(EvictionStrategy):
    """
    FIFOStrategyFastDelete is a variant of the FIFO eviction strategy
    that is faster on deleting keys,
    but slower in general.
    Use this if you expect to delete keys from the cache frequently.
    O(1) time complexity for deletes.
    """
    def __init__(self):
        self._order = OrderedDict()

    def add(self, key):
        self._order[key] = None

    def access(self, key):
        pass  # Not used by FIFO

    def evict(self) -> Any:
        if not self._order:
            raise Exception("No keys to evict")
        return self._order.popitem(last=False)[0]

    def remove(self, key):
        del self._order[key]
