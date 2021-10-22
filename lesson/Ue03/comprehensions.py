# -*- cod'ing: utf-8 -*-
"""
Created on Fri Oct 22 09:02:50 2021

@author: Andi
"""


divide = [x for x in range(1001) if x % 7 == 0]
print(divide)

with_three = [x for x in range(1001) if "3" in str(x)]
print(with_three)

doors = [(i**0.5) % 1 == 0 for i in range(1, 101)]
print(doors)

import calendar
months = [calendar.month_name[month] for month in range(1, 13)]
print(months)

monthsWithoutR = [calendar.month_name[month] for month in range(1, 13) if "r" not in calendar.month_name[month]]
print(monthsWithoutR)

cart = {(a, b) for a in {1, 3} for b in {"x", "y"}}
print(cart)

import string
ordLetters = {c : ord(c) for c in string.ascii_lowercase}
print(ordLetters)

