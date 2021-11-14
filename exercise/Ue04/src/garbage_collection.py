import sys

a = 1 # refs: 1
b = a # refs: 2

a = None # refs: 1
b = None # refs: 0

import sys

print(sys.getrefcount(1000)) # refs: 3
a = 1000
print(sys.getrefcount(a)) # refs: 4
a = None
print(sys.getrefcount(1000)) # refs: 3

import gc

gc.set_threshold(10, 10, 1)
gc.set_threshold(0, 0, 0)
collected_count = gc.collect()
collected_count = gc.collect(0)
collected_count = gc.collect(1)
collected_count = gc.collect(2)