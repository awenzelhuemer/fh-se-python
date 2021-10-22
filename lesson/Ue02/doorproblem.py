# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

doorList = [False] * 100

for run in range(100):
    for door in range(run, 100, run + 1):
            doorList[door] = not doorList[door]
    print(f"Doors {run + 1} open? {doorList[run]}")

# for i in range(10):
#    doorList[(i * i) - 1] = True

# for door in range(100):
#     if doorList[door]:
#         print(f"Doors {door + 1} open? {doorList[door]}")
# print(doorList)

for door in range(100):
    if (door + 1) ** 0.5 % 1 == 0:
        doorList[door] = True
    print(f"Doors {door + 1} open? {doorList[door]}")

tup = tuple(range(1, 11))
print(tup[-5: -2])