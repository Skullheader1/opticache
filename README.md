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

The project includes optimization tests to compare the performance of different approaches to implementing the same eviction strategy. **Those tests are not designed to show strengths and weaknesses of the strategy itself.** Run them with:
```bash
pip install -r ./optimization_tests/requirements.txt
pip install -e .
python optimization_tests/main.py
```

### Strategy Optimizations and effects

#### FIFO (First in first out)

A normal list shifts all elements on evict via `pop(0)`, making it O(n). Two optimized variants exist:
 
- **Deque**: `collections.deque` (implemented in C) provides O(1) `popleft` instead of shifting, but `remove(key)` is still O(n).
- **OrderedDict**: HashMap + Doubly Linked List gives O(1) for every operation, but has higher constant overhead than Deque.

| Operation | List | Deque | OrderedDict |
|---|---|---|---|
| add | O(1) | O(1) | O(1) |
| access | O(1) | O(1) | O(1) |
| evict | O(n) | O(1) | O(1) |
| remove | O(n) | O(n) | O(1) |

**Test results** (100k operations, 5 iterations):

| Operation | Deque | OrderedDict | List |
|---|---|---|---|
| Set | **0.18s** (fastest) | 0.21s (+16.7%) | 1.63s (+801.9%) |
| Delete | 81.81s (+36489.2%) | **0.22s** (fastest) | 79.38s (+35404.7%) |

**Result:** The Deque is the best choice for FIFO when `cache.delete()` is not frequently used, while the OrderedDict is better when frequent deletes on high capacity caches are expected.

#### LRU (Least recently used)

A normal list requires O(n) `remove` + `append` on every access. An `OrderedDict` provides O(1) `move_to_end`.

| Operation | List | OrderedDict |
|---|---|---|
| add | O(1) | O(1) |
| access | O(n) | O(1) |
| evict | O(n) | O(1) |
| remove | O(n) | O(1) |

**Test results** (100k operations, 5 iterations):

| Operation | Optimized | List-based | Speedup |
|---|---|---|---|
| Set | **0.046s** | 0.105s | 55.9% faster |
| Get | **0.020s** | 0.020s | 1.4% faster |
| Delete | **0.044s** | 15.591s | 99.7% faster |

#### LFU (Least frequently used)
A normal Dict tracks frequency per key, but evict needs to find the minimum O(n). Optimized through a Dict, a defaultdict(OrderedDict) and a min_freq integer pointer. The Dict maps keys to frequencies, the defaultdict groups keys by frequency and the min_freq points to the lowest active frequency
 
| Operation | Dict | Optimized |
|---|---|---|
| add | O(1) | O(1) |
| access | O(1) | O(1) |
| evict | O(n) | O(1) |
| remove | O(1) | O(1) |

**Test results** (100k operations, 5 iterations):

| Operation | Optimized | Dict-based | Speedup |
|---|---|---|---|
| Set | **0.049s** | 16.602s | 99.7% faster |
| Get | **0.020s** | 0.020s | 2.1% faster |
| Delete | 0.054s | **0.039s** | 35.5% slower |

**Result:** The optimized LFU is significantly faster for set operations due to O(1) eviction, but slightly slower for delete due to the overhead of maintaining the additional data structures. In total, the optimized version is a clear improvement and the loss in delete performance is a good tradeoff.

### Other optimizations:
- Threading: The `Cache` class is thread-safe and can be safely accessed by python threading.Thread.
- Memoization: Using the `@cache.memoize` decorator allows for automatic caching of function results, leading to significant performance improvements for expensive function calls with repeated arguments.

## Testing
Run the tests with:
```bash
pip install -r ./tests/requirements.txt
pip install -e .
pytest
```

## Usage of AI
- Github Copilot: Used in PyCharm for small code suggestions