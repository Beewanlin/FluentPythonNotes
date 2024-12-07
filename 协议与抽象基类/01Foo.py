"""
该例中，Foo类只实现序列协议的其中一个接口（只实现协议的一部分），即 __getitem__()方法，
但由于实现了序列协议的对象会被判断为可迭代对象，访问元素、迭代和使用in运算符都可用。
"""


class Foo:
    def __getitem__(self, pos):
        return range(0, 30, 10)[pos]


if __name__ == '__main__':
    f = Foo()
    print(f[1])  # 由于实现了__getitem__方法，可以返回f下标为1的元素
    for i in range(f):  # 虽然没有实现__iter__方法，但当要迭代f时，如果找不到__iter__方法，会调用__getitem__方法传入从0开始的整数尝试迭代
        print(f)
    print(20 in f)  # 虽然没有实现__container__方法，但此时会调用__getitem__方法迭代时检查是否有指定的元素
