"""
这里列举 functools 模块中常用且好用的几个装饰器。
例如：
functools.wraps
functolls.lru_cache
functools.singledispatch

引入并应用decoration_demo模块中的装饰器clock，计算程序运行的时间
"""

import functools
from 装饰器.decoration_demo.clock_decoration import clock

"""
lru_cache 意味着 least recently used cache。 
该装饰器适用于递归函数 将需要重复使用到的函数结果保存起来，避免入参相同时重复计算 从而避免耗时。
需要注意的一点是，该装饰器需要输入参数（没有入参需求，也需要带上空括号）。
它的两个参数为：maxsize, typed。
maxsize 代表 最大缓存大小（一般设置为2的幂次），超过这个限值后就会扔掉旧的结果，腾出新的缓存空间。
typed 代表 是否需要将不同类型的函数结果值分开存储，枚举值为True或False，例如 对1分别存储 整数 和 浮点数。
"""


@functools.lru_cache()
@clock
def fabonacci(n):
    if n < 2:
        return n
    else:
        return fabonacci(n - 1) + fabonacci(n - 2)


if __name__ == '__main__':
    print(fabonacci(6))
