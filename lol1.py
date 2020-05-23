import calendar
from datetime import datetime
target = int(input())

now = datetime.now()
month = now.month
year = now.year

while True:
    day = calendar.weekday(year, month, 1)
    if day == target:
        print(year, month)
        break
    month -= 1
    if month == 0:
        year -= 1
        month = 12
        