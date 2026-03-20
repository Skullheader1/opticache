import random
from typing import Any

from .base import EvictionStrategy


class RandomStrategy(EvictionStrategy):
    def __init__(self):
        self._keys = []

    def add(self, key):
        self._keys.append(key)

    def access(self, key):
        pass  # Not used by Random

    def evict(self) -> Any:
        if not self._keys:
            raise IndexError("No keys to evict")
        index = random.randint(0, len(self._keys) - 1)
        key = self._keys[index]
        self._keys[index] = self._keys[-1]
        self._keys.pop()
        return key

    def remove(self, key):
        index = self._keys.index(key)
        self._keys[index] = self._keys[-1]
        self._keys.pop()
