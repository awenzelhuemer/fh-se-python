print([x for x in range(1000) if x % 7 == 0])
print([x**0.5 for x in range(1, 101)])

with_three = [x for x in range(1001) if "3" in str(x)]
print(with_three)

doors = [(i**0.5) % 1 == 0 for i in range(1, 101)]
print(doors)

import calendar
months = [calendar.month_name[month] for month in range(1, 13)]
print(months)

import calendar
months = [calendar.month_name[month] for month in range(1, 13) if 'r' in calendar.month_name[month]]
print(months)

print([(a,b) for a in [1, 3] for b in ['x', 'y']])

import string
print({x:ord(x) for x in string.ascii_lowercase})
print({chr(x): x for x in range(ord('a'), ord('z') + 1)})