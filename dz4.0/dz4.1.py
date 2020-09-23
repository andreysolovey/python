from collections import deque
from random import randint
from functools import reduce


def odds(x):
    return x % 2 == 1


def evens(x):
    return x % 2 == 0


def primes(x):
    return x in {1, 2, 3, 5, 7}


def negated(x):
    return -x


def inverted(x):
    return 1/x


def squared(x):
    return x * x


def sum(a, b):
    return a + b


def multiply(a, b):
    return a * b


def join(a, b):
    from math import log10
    digits = int(log10(abs(b))) + 1
    return a * (10 ** digits) + b


def unite(a: set, b):
    a.add(b)
    return a


def reverse(a: deque, b):
    a.appendleft(b)
    return a


filters = {x.__name__: x for x in (odds, evens, primes)}
mappers = {x.__name__: x for x in (negated, inverted, squared)}
reducers = {x.__name__: x for x in (sum, multiply, join, unite, reverse)}
initials = {
    'sum': lambda: 0,
    'multiply': lambda: 1,
    'join': lambda: 0,
    'unite': set,
    'reverse': list
}


n = int(input('n = '))
numbers = [randint(1, 9) for i in range(n)]
print(numbers)

while True:
    reducer, mapper, predicate = input().split()
    initial = initials[reducer]
    reducer = reducers[reducer]
    mapper = mappers[mapper]
    predicate = filters[predicate]
    result = reduce(reducer, map(mapper, filter(predicate, numbers)), initial())
    print(result)
