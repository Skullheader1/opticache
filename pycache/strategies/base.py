from abc import ABC, abstractmethod
from typing import Any


class EvictionStrategy(ABC):
    # This method should be called whenever a key is added to the cache
    # to update the strategy's internal state
    @abstractmethod
    def add(self, key):
        pass

    # This method should be called whenever a key is accessed
    # (either read or write) to update the strategy's internal state
    @abstractmethod
    def access(self, key):
        pass

    # This method should return the key that needs to be evicted
    # based on the strategy's logic and
    # update the strategy's internal state accordingly.
    @abstractmethod
    def evict(self) -> Any:
        pass

    # This method should be called whenever a key ist manually removed
    # from the cache to update the strategy's internal state
    @abstractmethod
    def remove(self, key):
        pass
