from itertools import chain


def log(func):
    def wrapper(*args, **kwargs):
        r = func(*args, **kwargs)
        arg_str = ','.join(chain(map(str, args), map(lambda x: f'{x[0]}={x[1]}', kwargs.items())))
        print(f'{func.__name__}({arg_str}) -> {r}')
        return r
    return wrapper


@log
def a(x):
    return -x


@log
def b(x, y):
    return x * y


@log
def c(x, y, *args):
    result = x + y
    for arg in args:
        result += arg
    return result

a(1)
b(2, y=3)
c(1, 2, 3)

