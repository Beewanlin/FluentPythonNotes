"""
该版本使用itertools生成等差数列

itertools 有19个生成器函数。例如：
itertools.count(start, step)函数返回的生成器能生成一个起始于start步长为step的很多个数
itertools.takewhile(predicate, iterable)函数返回的生成器相比与itertools.count会判断iterable当前值在predicate中是否为真，如果为真则继续生成否则停止。
因此这里可以结合了两者构建一个生成等差数列的生成器。注意本例中aritprog_gen函数不是一个生成器函数，但它返回一个生成器，同样是一个生成器工厂函数。
"""
import itertools
    

def aritprog_gen(begin, step, end=None):
    first = type(begin + step)(begin)
    ap_gen = itertools.count(first, step)
    if end is not None:
        ap_gen = itertools.takewhile(lambda n: n < end, ap_gen)
    return ap_gen


if __name__ == '__main__':
    gen = aritprog_gen(0, .5, 2)
    print(list(gen))
