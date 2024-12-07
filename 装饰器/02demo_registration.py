"""
该demo说明 装饰器的一个特性是，Python加载模块时会立即运行装饰器。
若使用了装饰器，函数装饰器在导入模块的时候立刻运行，被装饰的函数只在明确调用时运行。（这突出了Python所谓的"导入时"和"运行时"的区别）
"""

registry = []


def register(func):
    print('running register(%s)' % func)
    registry.append(func)
    return func


# @register
def f1():
    print('running f1()')

# @register
def f2():
    print('running f2()')


def f3():
    print('running f3()')


def main():
    print('running main')
    print('registry——>', registry)
    f1()
    f2()
    f3()


if __name__ == '__main__':
    main()
