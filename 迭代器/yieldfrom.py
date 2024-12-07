"""
本例说明yield from
"""


def chain1(*iterable):
    for it in iterable:
        for i in it:
            yield i


def chain2(*iterable):
    """
    对chain1的改进，使用新引入的yield from句法，替代内层for循环。
    """
    for i in iterable:
        yield from i


if __name__ == '__main__':
    s = 'ABC'
    t = tuple(range(3))
    res1 = list(chain1(s, t))
    res2 = list(chain2(s, t))
    print(res1)
    print(res2)