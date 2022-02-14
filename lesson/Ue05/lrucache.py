from functools import lru_cache
from time import sleep
@lru_cache(maxsize=None)
def factorial(n):
    sleep(1)

    return n * factorial(n-1) if n else 1

print(factorial(10))
print(factorial(8))