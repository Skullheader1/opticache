# opticache

A Python caching library with pluggable eviction strategies.

## Installation

```bash
pip install opticache
```

### Usage

```python
from opticache import Cache
from opticache.strategies import (
    LRUStrategy,
    LFUStrategy,
    FIFOStrategy,
    FIFOStrategyFastDelete,
    RandomStrategy,
    SIEVEStrategy,
)

cache_lru = Cache(LRUStrategy, capacity=500)
cache_lfu = Cache(LFUStrategy, capacity=500)
cache_fifo = Cache(FIFOStrategy, capacity=500)
cache_sieve = Cache(SIEVEStrategy, capacity=500)

cache_lru.set(key, value)
cache_lru[key] = value
cache_lru.get(key)
value = cache_lru[key]

cache_lru.delete(key)

cache_lru.clear()

for i in cache_lru:
    print(i)


@cache_lru.memoize()
def foo(x):
    return x * 2


foo(10)  # Cache miss, computes result
foo(10)  # Cache hit, returns cached result
```

### Custom strategy

Implement the `EvictionStrategy` ABC to create your own:

```python
from opticache.strategies.base import EvictionStrategy


class MyStrategy(EvictionStrategy):
    def add(self, key):
        """Track a new key."""
        ...

    def access(self, key):
        """Update tracking when a key is accessed."""
        ...

    def evict(self):
        """Return the key to evict."""
        ...

    def remove(self, key):
        """Remove a key from tracking (manual delete)."""
        ...


from opticache import Cache

cache = Cache(MyStrategy, capacity=1000)
```

## Strategies

| Strategy | Evicts | Best for |
|---|---|---|
| `LRUStrategy` | Least recently used key | General purpose, rapidly changing access patterns |
| `LFUStrategy` | Least frequently used key | Stable popularity distributions (e.g. Zipf) |
| `FIFOStrategy` | Oldest key | Simple workloads, high throughput |
| `FIFOStrategyFastDelete` | Oldest key | FIFO with frequent `cache.delete()` calls |
| `RandomStrategy` | Random key | Unpredictable access patterns, low overhead | 
| `SIEVEStrategy` | Unvisited key via moving hand | Web caches, CDNs, filtering one-hit wonders |

### See the [Github repository](https://github.com/Skullheader1/opticache) for more details and tests.