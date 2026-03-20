# Last recently used strategy
import time
from typing import Any

import random

from opticache.strategies import (EvictionStrategy,
                                  FIFOStrategy,
                                  FIFOStrategyFastDelete)
from opticache import Cache


class FIFOStrategyList(EvictionStrategy):
    def __init__(self):
        self._queue = []

    def add(self, key):
        self._queue.append(key)

    def access(self, key):
        pass  # Not used by FIFO

    def evict(self) -> Any:
        if not self._queue:
            raise Exception("No keys to evict")
        return self._queue.pop(0)

    def remove(self, key):
        self._queue.remove(key)


def run_test(iterations, level):
    time1_set = 0
    time1_get = 0

    time2_set = 0
    time2_get = 0

    time3_set = 0
    time3_get = 0

    for _ in range(iterations):
        cache1 = Cache(FIFOStrategy, int(level/2))
        cache2 = Cache(FIFOStrategyList, int(level/2))
        cache3 = Cache(FIFOStrategyFastDelete, int(level/2))
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
        start = time.time()

        for i in range(level):
            cache3.set(f'key{i}', f'value{i}')
        time3_set += time.time() - start
        start = time.time()
        for i in range(level):
            cache3.get(f'key{i % int(level / 10)}')
        time3_get += time.time() - start

    time1_delete_existing = 0
    time2_delete_existing = 0
    time3_delete_existing = 0

    for i in range(iterations):
        # Fill caches
        cache1 = Cache(FIFOStrategy, level)
        cache2 = Cache(FIFOStrategyList, level)
        cache3 = Cache(FIFOStrategyFastDelete, level)
        for i in range(level):
            cache1.set(f'key{i}', f'value{i}')
            cache2.set(f'key{i}', f'value{i}')
            cache3.set(f'key{i}', f'value{i}')

        # Random order of deletes to avoid best/worst case scenarios
        # for list-based FIFO / deque-based FIFO
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

        start = time.time()
        for i in delete_order:
            cache3.delete(f'key{i}')
        time3_delete_existing += time.time() - start

    def print_ranked(label, times):
        fastest_time = min(times.values())
        print(f"=== {label} ===")
        for i, (name, t) in enumerate(sorted(times.items(),
                                             key=lambda x: x[1]), 1):
            if fastest_time == 0 or t == 0:
                slower_pct = 0.0
            else:
                slower_pct = (t - fastest_time) / fastest_time * 100
            marker = " (fastest)" if t == fastest_time \
                else f" (+{slower_pct:.1f}%)"
            print(f"  {i}. {name}: {t:.4f}s{marker}")
        print()

    print_ranked("Set times", {
        "Deque FIFO": time1_set,
        "List FIFO": time2_set,
        "OrderedDict FIFO": time3_set,
    })

    print_ranked("Get times", {
        "Deque FIFO": time1_get,
        "List FIFO": time2_get,
        "OrderedDict FIFO": time3_get,
    })

    print_ranked("Delete existing keys", {
        "Deque FIFO": time1_delete_existing,
        "List FIFO": time2_delete_existing,
        "OrderedDict FIFO": time3_delete_existing,
    })


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
