import random
n = int(input())
x = []
for i in range(n):
    x.append(random.randint(-5, 5))
for i in x:
    if i == 0:
        x.insert(0, i)
    else:
        pass
print(x)
