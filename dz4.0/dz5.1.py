from functools import reduce


def multiply(func):
    def wrapper(*args):
        return func(reduce(lambda x, y: x * y, args))
    return wrapper


@multiply
def func(x):
    print(x)


numbers = list(map(int, input().split()))
func(*numbers)

