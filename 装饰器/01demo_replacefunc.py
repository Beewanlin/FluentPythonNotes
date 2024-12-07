"""
该demo说明，装饰器的本质是入参为函数的函数，返回/出参也可以是函数。
其表现看就是<被装饰的函数>被丰富了<装饰器>的那部分功能。如果装饰器返回是一个函数的话，那么被装饰的函数实际上是被替换了，见下例。
"""


def deco(func):
    def inner():
        print('running inner funcion')
    return inner

@deco
def func():
    print('running func function')


if __name__ == '__main__':
    func()