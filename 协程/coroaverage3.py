"""
该例基于coroaverage2.py，改进获取协程返回值的方式。

相比于coroaverage2.py例子中，try/else手动捕获stopIteration异常并获取其value值以获取协程的返回值，
本例使用yield from自动捕获stopIteration异常。

yield from结构：
委派生成器：含有 yield from 表达式的生成器函数
子生成器：实际接收值 和 产出值的生成器，是委派生成器委派的对象 yield from <iterable> 中的 <iterable> 部分获取的生成器
调用方/客户端：调用委派生成器的模块
"""


from 协程.coroutil import coroutine
from collections import namedtuple


Result = namedtuple('Result', 'count average')


# 这里不能用预激装饰器 @coroutine，因为yield from会自动预激，两者会冲突
def averager():
    """
    子生成器
    """
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total/count
    return Result(count, average)


def grouper(results, key):
    """
    这里委派生成器的作用较大。
    （使用yield from，就不需要手动预激子生成器了。）
    调用方/客户端每次调用委派生成器时，先执行到 yield from 右边的表达式，调用子生成器实例，然后暂停；把控制权转交给调用方main
    等子生成器作为协程在运行完毕后，直接获取返回的值（不需手动捕获StopIteraion异常），绑定在 yield from 的左式上。
    """
    while True:   # 每次迭代新建一个averager实例，是一个生成器对象，作为协程使用
        results[key] = yield from averager()  # step3-（自动预激）调用子生成器 并等待返回值再赋值。


def main(data):
    """
    调用方/客户端
    """
    results = {}
    for key, values in data.items():
        group = grouper(results, key)  # 获取委派生成器group
        next(group)  # 预激委派生成器
        for value in values:
            group.send(value)  # 传值给group，但实际上group不会知道传入的值是什么，委派生成器group起管道的作用，调用方可以直接把值传给子生成器
        group.send(None)  
    # print(results)
    report(results)


def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(
            result.count, group, result.average, unit
        ))


data = {
    'girls;kg':
        [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m':
        [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg':
        [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.1, 40.6, 36.3],
    'boys;m':
        [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46]
}


if __name__ == '__main__':
    main(data)