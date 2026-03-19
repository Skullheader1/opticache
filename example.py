from pycache import Cache
from pycache.strategies import LRUStrategy, LFUStrategy

cache = Cache(LRUStrategy, capacity=3)

cache.set("user:42", {"name": "Max", "role": "admin"})
cache.set("user:7", {"name": "James", "role": "user"})

print("User 42: " + str(cache.get("user:42"))) # This will return the user data for user:42, as it was recently added to the cache
print("User 99: " + str(cache.get("user:99"))) # This will return None, as it was never added to the cache

cache.set("user:17", {"name": "Raph", "role": "user"})
cache.set("user:3", {"name": "Don", "role": "user"})

print("User 7: " + str(cache.get("user:7")))  # This will be no longer in the cache, as it was the least recently used item and the cache capacity is 3
print("User 42: " + str(cache.get("user:42"))) # This will still be in the cache, as it was recently accessed

for i in cache:
    print(i) # This will print the key and the value for each item as a tuple

print(len(cache)) # This will print the number of items currently in the cache
