"""
最简单的协程举例：
"""


def simple_coroutine():
    print('--> coroutine started')
    x = yield
    print('--> coroutine received: ', x)


def simple_coroutine2(a):
    print('--> started：a=', a)
    b = yield a
    print('--> received: b=', b)
    c = yield a + b
    print('--> received: c=', c)


if __name__ == '__main__':
    # case1：最简单的协程举例
    my_coro = simple_coroutine()
    print(my_coro)
    print(next(my_coro))
    print(my_coro.send(42))
    # case2：产出两个值的协程，根据此例说明执行协程的各个阶段及状态。
    my_coro2 = simple_coroutine2(14)
    print(next(my_coro2))
    print(my_coro2.send(99))
    print(my_coro2.send(9))
