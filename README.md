# pycache

A Python caching library with pluggable eviction strategies and a optimization tests to demonstrate the impact of data structure choices.

## Installation

```bash
pip install -e .
```

## Quick start

[Click here to view the example.py](example.py)

## Strategies

| Strategy | Evicts | Best for |
|---|---|---|
| `LRUStrategy` | Least recently used key | General purpose, rapidly changing access patterns |
| `LFUStrategy` | Least frequently used key | Stable popularity distributions (e.g. Zipf) |
| `FIFOStrategy` | Oldest key | Simple workloads, high throughput |
| `FIFOStrategyFastDelete` | Oldest key | FIFO with frequent `cache.delete()` calls |
| `RandomStrategy` | Random key | Unpredictable access patterns, low overhead | 
| `SIEVEStrategy` | Unvisited key via moving hand | Web caches, CDNs, filtering one-hit wonders |

### Usage

```python
from pycache import Cache
from pycache.strategies import (
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
```

### Custom strategy

Implement the `EvictionStrategy` ABC to create your own:

```python
from pycache.strategies.base import EvictionStrategy

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

from pycache import Cache
cache = Cache(MyStrategy, capacity=1000)
```

## Optimization tests

The project includes optimization tests to compare the performance of different approaches to implementing the same eviction strategy. <b>Those tests are not designed to how strengths and weaknesses of the strategy itself.</b> Run them with:
```bash
pip install -r ./optimization_tests/requirements.txt
pip install -e .
python optimization_tests/main.py
```

### Optimizations and effects
- `LRUStrategy`:
  - A normal Array shifts elements on access -> O(1) add time, O(n) access time,  O(n) evict time and O(n) remove time.
  - Optimized through a OrderedDict: A HashMap + Doubly Linked List allows O(1) time complexity for every operation.
- `LFUStrategy`:
  - A normal Dict tracks frequency per key, but evict needs to find the minimum -> O(1) add time, O(1) access time, O(n) evict time and O(1) remove time.
  - Optimized through a Dict, a defaultdict(OrderedDict) and a min_freq integer pointer. The Dict maps keys to frequencies, the defaultdict groups keys by frequency and the min_freq points to the lowest active frequency -> O(1) time complexity for every operation.
- `FIFOStrategy:`
  - A normal Array shifts all elements on evict via pop(0) -> O(1) add time, O(1) access time, O(n) evict time and O(n) remove time.
  - Optimized through a Deque: A doubly linked list allows O(1) popleft instead of shifting -> O(1) add time, O(1) access time, O(1) evict time and O(n) remove time.
    - Collections.deque is implemented in C, making it much faster than a regular python list
  - Optimized through a OrderedDict: A HashMap + Doubly Linked List allows O(1) time complexity for every operation, but is slower than a Deque due to the overhead of maintaining the hash map.
