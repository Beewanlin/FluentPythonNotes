"""
此版本较于之前版本mirror_gen.py，新增了对于异常的处理。

因为对于使用@contextlib.contextmanager实现的上下文管理器，若在with语句块中遇到了异常，会在yield语句中抛出。
如果不处理该异常的话，被装饰的函数会在yield句终止。
"""
import contextlib


@contextlib.contextmanager
def looking_glass():
    import sys
    original_write = sys.stdout.write

    def reverse_write(text):  # 定义自定义的函数
        original_write(text[::-1])  # 在闭包中可以访问original_write

    sys.stdout.write = reverse_write
    try:
        yield 'JABBERWOCKY'
    except ZeroDivisionError:
        msg = 'Please DO NOT divide by zero'
    finally:
        sys.stdout.write = original_write
        if msg:
            print(msg)


if __name__ == '__main__':
    with looking_glass() as what:
        print('Alice, Kitty and Snowdrop')
        print(what)
    print(what)