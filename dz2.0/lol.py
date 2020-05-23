import calendar
x = input('Введите дату вашего рождения')
y = x.split('.')

day = int(y[0])
month = int(y[1])
year = int(y[2])
weekday = calendar.weekday(year, month, day)
print(weekday)
