"""
使用try/finally块，使得协程不论以什么方式终止，终止时都必须执行finally中的相关操作
"""
from inspect import getgeneratorstate


class DemoException(Exception):
    """
    为了此例演示定义的异常
    """


# 定义协程
def demo_exc_handling():
    print('-> coroutine started')
    try:
        while True:
            try:
                x = yield
            except DemoException:
                print('*** DemoException handled. Continuing...')
            else:
                print('-> coroutine received:{!r}'.format(x))
    finally:
        print('-> coroutine ending')


if __name__ == '__main__':
    exc_coro = demo_exc_handling()
    next(exc_coro)
    exc_coro.send(1)
    exc_coro.throw(DemoException)  # 给协程传入可以处理的异常，不会导致协程停止
    print(getgeneratorstate(exc_coro))
    exc_coro.throw(ZeroDivisionError)  # 给协程传入无法处理的异常，协程会向上冒泡 并终止
    print(getgeneratorstate(exc_coro))
