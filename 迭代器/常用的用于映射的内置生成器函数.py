"""
该文档说明用于映射的生成器函数，返回具有映射作用的生成器
"""
import itertools
import operator

if __name__ == '__main__':
    sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]
    """
    itertools.accumulate(it[,func]) 产出累计的总和。
    如果提供了func，则将结果的第n-1个元素和it的第n个元素传给func，得到映射后的第n个结果
    （特殊情况 n=1时，即结果的第一个元素，是it的第一个元素，不映射）
    """
    # 计算数列的总和
    res1 = list(itertools.accumulate(sample))
    # 计算数列的最小值
    res2 = list(itertools.accumulate(sample, min))
    # 计算数列的最大值
    res3 = list(itertools.accumulate(sample, max))
    # 计算数列的乘积
    res4 = list(itertools.accumulate(sample, operator.mul))
    # 计算1!、2!、……、10！的阶乘
    res5 = list(itertools.accumulate(range(1, 11), operator.mul))
    print(res1)
    print(res2)
    print(res3)
    print(res4)
    print(res5)
    """
    enumerate(iterable, start=0) 产出由2个元素组成的元组，
    元组中的第一个元素是从start开始逐个加1的序号，元组中的第二个元素是可迭代对象iterable中的元素
    """
    res = list(enumerate('albatroz', 1))
    print(res)
    """
    map(func, it1[, it2, ... itN]) 把it中的各个元素传给func，产出结果；
    如果传入N个元素，func必须要能接收N个参数；如果多个可迭代对象长度不等，映射结果以最短的长度为准。
    """
    # 从0到10计算各个整数的平方
    res1 = list(map(operator.mul, range(11), range(11)))
    print(res2)
    # 生成元组
    res2 = list(map(lambda a, b: (a, b), range(1, 11), [2, 3, 4]))
    print(res2)
    """
    itertools.starmap(func, it) 把it中的各个元素传给func，产出结果；
    输入的可迭代对象应该产出可迭代的元素iit，然后以func(*iit)的形式调用func。因此it元素通常也是生成器对象。
    """
    # 从1开始，根据字母所在的位置，重复相应的次数
    res1 = list(itertools.starmap(operator.mul, enumerate('abcde', 1)))
    print(res1)
    res2 = list(itertools.starmap(lambda a, b: b/a, enumerate(itertools.accumulate(sample), 1)))
    print(res2)