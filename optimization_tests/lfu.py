# Last recently used strategy
import time
from typing import Any

import random

from pycache.strategies import EvictionStrategy, LFUStrategy
from pycache import Cache


class LFUStrategyDict(EvictionStrategy):
    def __init__(self):
        self._keys = {}

    def add(self, key):
        self._keys[key] = 1

    def access(self, key):
        self._keys[key] += 1

    def evict(self) -> Any:
        if not self._keys:
            raise IndexError("No keys to evict")
        key = min(self._keys, key=self._keys.get)
        del self._keys[key]
        return key

    def remove(self, key):
        self._keys.pop(key)


def run_test(iterations, level):
    time1_set = 0
    time1_get = 0
    time2_set = 0
    time2_get = 0

    for _ in range(iterations):
        cache1 = Cache(LFUStrategy, int(level/10))
        cache2 = Cache(LFUStrategyDict, int(level/10))
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
        cache1 = Cache(LFUStrategy, level)
        cache2 = Cache(LFUStrategyDict, level)
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
    print(f"Optimized LFU strategy average time: "
          f"{time1_set / iterations:.4f} seconds")
    print(f"Dict-based LFU strategy average time: "
          f"{time2_set / iterations:.4f} seconds")
    speedup_set = (time2_set - time1_set) / time2_set * 100 \
        if time2_set != 0 else 0
    print(f"Optimized is {abs(speedup_set):.1f}% "
          f"{'faster' if speedup_set > 0 else 'slower'}")

    print("\n\n=== Get times ===")
    print(f"Optimized LFU strategy average time: "
          f"{time1_get / iterations:.4f} seconds")
    print(f"Dict-based LFU strategy average time: "
          f"{time2_get / iterations:.4f} seconds")
    speedup_get = (time2_get - time1_get) / time2_get * 100 \
        if time2_get != 0 else 0
    print(f"Optimized is {abs(speedup_get):.1f}% "
          f"{'faster' if speedup_get > 0 else 'slower'}")

    print("\n\n=== Delete times ===")
    print(f"Optimized LFU strategy average time: "
          f"{time1_delete_existing / iterations:.4f} seconds")
    print(f"Dict-based LFU strategy average time: "
          f"{time2_delete_existing / iterations:.4f} seconds")
    speedup_delete_existing = ((time2_delete_existing - time1_delete_existing)
                               / time2_delete_existing * 100) \
        if time2_delete_existing != 0 else 0
    print(f"Optimized is {abs(speedup_delete_existing):.1f}% "
          f"{'faster' if speedup_delete_existing > 0 else 'slower'}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("iterations",
                        type=int,
                        help="Number of iterations to run")
    parser.add_argument("load",
                        type=int,
                        help="Number of items to load into the cache")
    args = parser.parse_args()
    run_test(args.iterations, args.load)
