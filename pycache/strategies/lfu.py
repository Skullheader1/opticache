from collections import defaultdict, OrderedDict
from typing import Any

from pycache.strategies.base import EvictionStrategy

class LFUStrategy(EvictionStrategy):
    """
    LFU (Least Frequently Used) eviction strategy implementation.
    This strategy evicts the key that has been accessed the least number of times.
    """
    def __init__(self):
        self._key_freq = {}
        self._freq_keys = defaultdict(OrderedDict)
        self._min_freq = 0

    def add(self, key):
        self._key_freq[key] = 1
        self._freq_keys[1][key] = None
        self._min_freq = 1

    def access(self, key):
        freq = self._key_freq[key]
        del self._freq_keys[freq][key]
        if not self._freq_keys[freq]:
            del self._freq_keys[freq]
            if self._min_freq == freq:
                self._min_freq += 1
        freq += 1
        self._key_freq[key] = freq
        self._freq_keys[freq][key] = None

    def evict(self) -> Any:
        if not self._key_freq:
            raise IndexError("No keys to evict")
        victims = self._freq_keys[self._min_freq]
        key, _ = victims.popitem(last=False)
        if not victims:
            del self._freq_keys[self._min_freq]
        del self._key_freq[key]
        return key

    def remove(self, key):
        freq = self._key_freq.pop(key)
        del self._freq_keys[freq][key]
        if not self._freq_keys[freq]:
            del self._freq_keys[freq]
            if self._min_freq == freq:
                self._min_freq = min(self._freq_keys) if self._freq_keys else 0
