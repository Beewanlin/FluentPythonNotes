"""
此例说明@contextmanager装饰器，改写mirror上下文管理器类，使用该装饰器能减少大量代码量。
"""
import contextlib


@contextlib.contextmanager
def looking_glass():
    import sys
    original_write = sys.stdout.write

    def reverse_write(text):  # 定义自定义的函数
        original_write(text[::-1])  # 在闭包中可以访问original_write

    sys.stdout.write = reverse_write
    yield 'JABBERWOCKY'  # yield生成的是让__enter__返回的值。yield之前相当于是__enter__方法，yield之后相当于是__exit__方法。
    sys.stdout.write = original_write


if __name__ == '__main__':
    with looking_glass() as what:
        print('Alice, Kitty and Snowdrop')
        print(what)
    print(what)