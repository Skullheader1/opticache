#Last recently used strategy
import random
import time
from typing import Any

from pycache.strategies import EvictionStrategy, LRUStrategy
from pycache import Cache


class LRUStrategyList(EvictionStrategy):
    def __init__(self):
        self._order = []

    def add(self, key):
        self._order.append(key)

    def access(self, key):
        self._order.remove(key)
        self._order.append(key)

    def evict(self) -> Any:
        if not self._order:
            raise IndexError("No keys to evict")
        return self._order.pop(0)

    def remove(self, key):
        self._order.remove(key)




iterations = 3
level = 100000

time1_set = 0
time1_get = 0
time2_set = 0
time2_get = 0

for i in range(iterations):
    cache1 = Cache(LRUStrategy, int(level/10))
    cache2 = Cache(LRUStrategyList, int(level/10))
    start = time.time()

    for i in range(level):
        cache1.set(f'key{i}', f'value{i}')
    time1_set += time.time() - start
    start = time.time()
    for i in range(level):
        cache1.get(f'key{i % int(level / 10)}')

    time1_get += time.time() - start
    start = time.time()

    for i in range(level):
        cache2.set(f'key{i}', f'value{i}')
    time2_set += time.time() - start
    start = time.time()
    for i in range(level):
        cache2.get(f'key{i % int(level / 10)}')

    time2_get += time.time() - start

time1_delete_existing = 0
time2_delete_existing = 0

for i in range(iterations):
    cache1 = Cache(LRUStrategy, level)
    cache2 = Cache(LRUStrategyList, level)
    for i in range(level):
        cache1.set(f'key{i}', f'value{i}')
        cache2.set(f'key{i}', f'value{i}')

    delete_order = list(range(level))
    random.shuffle(delete_order)

    start = time.time()
    for i in delete_order:
        cache1.delete(f'key{i}')
    time1_delete_existing += time.time() - start

    start = time.time()
    for i in delete_order:
        cache2.delete(f'key{i}')
    time2_delete_existing += time.time() - start

print("=== Set times ===")
print(f"Optimized LRU strategy average time: {time1_set / iterations:.4f} seconds")
print(f"Dict-based LRU strategy average time: {time2_set / iterations:.4f} seconds")
speedup_set = (time2_set - time1_set) / time2_set * 100
print(f"Optimized is {abs(speedup_set):.1f}% {'faster' if speedup_set > 0 else 'slower'}")

print("\n\n=== Get times ===")
print(f"Optimized LRU strategy average time: {time1_get / iterations:.4f} seconds")
print(f"Dict-based LRU strategy average time: {time2_get / iterations:.4f} seconds")
speedup_get = (time2_get - time1_get) / time2_get * 100
print(f"Optimized is {abs(speedup_get):.1f}% {'faster' if speedup_get > 0 else 'slower'}")

print("\n\n=== Delete times ===")
print(f"Optimized LRU strategy average time: {time1_delete_existing / iterations:.4f} seconds")
print(f"Dict-based LRU strategy average time: {time2_delete_existing / iterations:.4f} seconds")
speedup_delete_existing = (time2_delete_existing - time1_delete_existing) / time2_delete_existing * 100
print(f"Optimized is {abs(speedup_delete_existing):.1f}% {'faster' if speedup_delete_existing > 0 else 'slower'}")