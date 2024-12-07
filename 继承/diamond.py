"""
多重继承，命名冲突问题（不相关的祖先类有同名的方法实现时，会出现调用问题）。
"""
import numbers
import tkinter


class A:
    def ping(self):
        print('ping: ', self)


class B(A):
    def pong(self):
        print('pong: ', self)


class C(A):
    def pong(self):
        print('PONG: ', self)


class D(B, C):

    def ping(self):
        super().ping()  # 使用super()函数调用ping方法，将该调用委托给A类。
        print('post-ping: ', self)

    def pingpong(self):
        self.ping()
        super().ping()  # 使用super()函数调用ping方法，跳过D类的ping方法，找到A类的ping方法。
        self.pong()  # 根据__mro__，找到的是B类实现的pong方法。
        super().pong()  # 根据__mro__，找到的也是B类实现的pong方法。
        C.pong(self)  # 忽略__mro__，直接调用C类实现的方法。


def print_mro(cls):
    print(', '.join(c.__name__ for c in cls.__mro__))


if __name__ == '__main__':
    d = D()
    print(d.pong())  # D类继承了B类和C类，直接调用实例d的pong方法，实际上调用的是B类中的pong方法。
    print(C.pong(d))  # 调用D类的超类C中的方法，可以直接调用，把实例d作为显示参数传入即可。
    print(D.__mro__)  # 记录类的【方法解析顺序】，从当前类开始，一直向上列出各个超类直到object类。
    print(d.ping())
    print(d.pingpong())
    # 查看类的__mro__属性
    print_mro(bool)
    print_mro(numbers.Integral)
    print(tkinter.Text)  # tkinter的Text类具有复杂的多重继承。
