"""
此例说明executor.map方法如何运用于并发调用。

executor.map(fn, *iterables)返回的是生成器，但它有个特性是 其返回的结果的顺序和调用顺序需一致。
这就导致如果调用顺序在后但先生成结果的话，不会先返回这个结果，而是要等调用顺序在前的调用结果，按顺序输出。
要先输出先产出的结果，可以使用futures.submit和futures.as_completed的组合来替代Executor.map实现
"""
from time import sleep, strftime  # strftime是专门用来格式化事件元组的函数
from concurrent import futures


def display(*args):
    print(strftime('[%H:%M:%S]'), end='')
    print(*args)


def loiter(n):
    msg = '{}loiter({}): doing nothing for {}s...'
    display(msg.format('\t'*n, n, n))
    sleep(n)
    msg = '{}loiter({}): done.'
    display(msg.format('\t'*n, n))  # display相比于print，能支持更多格式的包括文本、图像、表格等的输出，后者只能在控制台输出文本
    return n*10


def main():
    display('Script starting.')
    executor = futures.ThreadPoolExecutor(max_workers=3)
    results = executor.map(loiter, range(2))
    display('results:', results)
    display('Waiting for individual results:')
    for i, result in enumerate(results):
        display('result {}: {}'.format(i, result))


if __name__ == '__main__':
    main()