from pycache import Cache
from pycache.strategies import LRUStrategy, LFUStrategy

cache_lru = Cache(LRUStrategy, capacity=50000)

for i in range(1000000):
    cache_lru.set(f'key{i}', f'value{i}')

cache_lfu = Cache(LFUStrategy, capacity=50000)

for i in range(1000000):
    cache_lfu.set(f'key{i}', f'value{i}')
