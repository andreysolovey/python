from random import randint
y = randint(0, 10)

while True:
     x = int(input('Введите число'))
     if x > y:
         print('число больше')
     elif x < y:
         print('Число меньше')
     else:
         print('Вы угадали число')
         break
