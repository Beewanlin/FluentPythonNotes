"""
实现一个简单的装饰器，记录函数运行的起始时间。

装饰器的特点：
"""
import time


def clock(func):
    def clocked(*args):
        t0 = time.perf_counter()  # 该函数 具有最高可用分辨率的时钟，适用于代码性能测试
        result = func(*args)  # 让被计时函数运行
        elasped = time.perf_counter() - t0  # 计时结束，计算时间差

        name = func.__name__  # 输出结果
        arg_str = ','.join(repr(arg) for arg in args)  # repr函数 将python对象解释为解释器可读的形式
        print('[%0.8fs]%s(%s)->%s' % (elasped, name, arg_str, result))
        return result
    return clocked

