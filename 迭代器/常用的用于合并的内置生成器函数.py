"""
该文档说明用于合并的生成器函数，返回具有映射作用的生成器
"""
import itertools
import operator

if __name__ == '__main__':
    """
    itertools.chain(it1, it2,..., itN) 依次无缝产出itN中的所有元素。如果只传入一个参数，则该函数不会起什么作用。
    """
    res = list(itertools.chain('ABC', range(2)))
    print(res)
    """ 
    itertools.chain.from_iterable(it) 要求可迭代对象it中的各个元素也是可迭代的，该函数产出it元素中的各个元素
    """
    res = list(itertools.chain.from_iterable(enumerate('ABC')))
    print(res)
    """
    zip(it1, ..., itN) 并行处理多个可迭代对象，从各个可迭代对象中获取元素，产出由N个元素组成的元组。
    若多个可迭代元素的长度不同，产出结果以最短的为准。
    """
    res1 = list(zip('ABC', range(5)))
    res2 = list(zip('ABC', range(5), [10, 20, 30, 40]))
    print(res1)
    print(res2)
    """
    itertools.zip_longest(it1, ..., itN, fillvalue=None) 和上一个zip方法类似，不过它的产出结果以最长的为准，不足的用fillvalue部族。
    """
    res1 = list(itertools.zip_longest('ABC', range(5)))
    res2 = list(itertools.zip_longest('ABC', range(5),fillvalue='?'))
    print(res1)
    print(res2)
    """
    itertools.product计算笛卡尔积的生成器。
    """
    res1 = list(itertools.product('AB', range(2)))
    print(res1)
    # 参数repeat表示重复处理几次
    res2 = list(itertools.product('AB', repeat=2))
    res3 = list(itertools.product(range(2), repeat=2))
    res4 = list(itertools.product(range(2), repeat=3))
    print(res2)
    print(res3)
    print(res4)
    rows = itertools.product('AB', range(2), repeat=2)
    for row in rows:
        print(row)