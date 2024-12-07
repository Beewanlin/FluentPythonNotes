"""
该例基于coroaverage1.py，新增了终止协程的判断，新增了协程的返回且不在yield产出值。

在该例中，要终止协程然后获取协程的返回值，需要输入None 然后在抛出的StopIteration异常对象的value值中获取到协程的返回值。
"""


from 协程.coroutil import coroutine
from collections import namedtuple


Result = namedtuple('Result', 'count average')

@coroutine
def averager():
    total = 0
    count = 0
    average = 0
    while True:
        value = yield
        if value is None:
            break
        total += value
        count += 1
        average = total/count
    return Result(count, average)


if __name__ == '__main__':
    coroaverage = averager()
    print(coroaverage.send(10))
    print(coroaverage.send(12))
    print(coroaverage.send(13))
    # 传入None会终止循环，导致协程结束，返回结果。但生成器对象会抛出StopIteration异常，异常对象的value属性保存着返回的值。
    # print(coroaverage.send(None))
    # 要获取返回的值，需捕获StopIteration异常（其标准做法是使用yield from来处理）
    try:
        coroaverage.send(None)
    except StopIteration as exc:
        result = exc.value
    print(result)