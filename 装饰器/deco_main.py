from 装饰器.decoration_demo.clock_decoration import clock
import time


@clock
def snooze(seconds):
    time.sleep(seconds)


@clock
def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)


if __name__ == '__main__':
    snooze(2)
    factorial(2)
