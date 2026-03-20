import threading
import time

from opticache import Cache
from opticache.strategies import LRUStrategy, LFUStrategy

print("=== Basic cache operations example ===\n")

cache = Cache(LRUStrategy, capacity=3)

cache.set("user:42", {"name": "Max", "role": "admin"})
cache.set("user:7", {"name": "James", "role": "user"})

# This will return the user data for user:42
print("User 42: " + str(cache.get("user:42")))
# This will return None, as it was never added to the cache
print("User 99: " + str(cache.get("user:99")))

cache.set("user:17", {"name": "Raph", "role": "user"})
cache.set("user:3", {"name": "Don", "role": "user"})

# This will be no longer in the cache,
# as it was the least recently used item and the cache capacity is 3
print("User 7: " + str(cache.get(
    "user:7")))
# This will still be in the cache, as it was recently accessed
print("User 42: " + str(cache.get("user:42")))

print("== Printing all items in cache ==")
for i in cache:
    print(i)  # This will print the key and the value for each item as a tuple

# This will print the number of items currently in the cache
print("Length of cache: " + str(len(cache)))

print("\n\n=== Threading example ===\n")

cache2 = Cache(LRUStrategy, capacity=100)


def worker(id):
    for i in range(2):
        cache2.set(f"thread{id}_key{i}", f"value{i}")
        # Simulates an input/output operation,
        # causing another thread to run operations on the cache in this time
        time.sleep(
            0.001)


threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print("== Printing all items in cache2 ==")
for i in cache2:
    print(i)

print("\n\n=== Cache operations examples ===\n")

cache3 = Cache(LRUStrategy, capacity=10)

cache3.set("key1", "value1")  # You can set items this way
cache3["key2"] = "value2"  # You can also set items this way
cache3["key3"] = "value3"
cache3["key4"] = "value4"

# You can get items this way
print("One way to get an item: " + cache3.get("key1"))
# You can also get items this way
print("Other way to get an item: " + cache3["key2"])

cache3.delete("key1")  # You can delete items this way
del cache3["key2"]  # You can also delete items this way

print("key3 in cache3: " + str("key3" in cache3))
cache3.delete("key3")
print("key3 in cache3: " + str("key3" in cache3))

print("Entries in cache3 before clear: " + str(len(cache3)))
cache3.clear()  # This will clear all items from the cache
print("Entries in cache3 after clear: " + str(len(cache3)))

cache4 = Cache(LFUStrategy, capacity=10)

print("\n\n=== Memoization example ===\n")


@cache4.memoize()
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


print("First call to fibonacci(35):")
start = time.time()
# This will calculate the result and cache it
print("fibonacci(35) = " + str(fibonacci(35)))
print(f"Time taken: {time.time() - start:.4f} seconds")

print("\nSecond call to fibonacci(35):")
start = time.time()
# This will get the cached result without calculating it again
print("fibonacci(35) = " + str(fibonacci(35)))
print(f"Time taken: {time.time() - start:.4f} seconds")
