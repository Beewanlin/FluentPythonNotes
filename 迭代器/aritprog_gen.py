"""
等差数列生成器
该版本直接实现一个生成器函数（如果一个类是为了构建生成器而去实现__iter__函数，那还不如直接实现一个生成器函数）
"""


def aritprog_gen(begin, step, end=None):
    result = type(begin + step)(begin)
    index = 0
    forever = end is None
    while forever or result < end:
        yield result
        index += 1
        result = begin + step * index


if __name__ == '__main__':
    gen = aritprog_gen(0, 1, 3)
    print(list(gen))
    print(list(aritprog_gen(0, .5, 2)))
