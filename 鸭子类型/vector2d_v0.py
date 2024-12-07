from array import array
import math


class Vector2d:
    """
    常用typecode：
    'd'：双精度浮点数
    'f'：单精度浮点数
    'I'：无符号整数
    'i'：带符号整数
    'h'：带符号短整形整数
    'B'：无符号字符
    'b'：带符号字符
    """
    typecode = 'd'  # 类属性typecode，表示类型码。例如，短整形有符号整数的类型码为'h'，无符号字符的类型码为'B'。

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __iter__(self):
        # 为了实现拆包，从Vector2d实例中产出分量self.x 和 self.y，需要将Vector2d实例实现为可迭代的。
        # 而定义可迭代的对象，就要实现__iter__()方法
        return (i for i in (self.x, self.y))

    def __abs__(self):
        return math.hypot(self.x, self.y)  # math包中有专门的函数hypot 用来计算直角三角形的斜边长

    def __repr__(self):
        class_name = type(self).__name__
        return "{}({!r}, {!r})".format(class_name, *self)  # 这里 *self 会将x和y分量提供给format函数。{!r}等效于%r

    def __str__(self):
        # return str((self.x, self.y))  # 相比于该方法，下面行直接用tuple实现更聪明，因为本身就需要实现类实例的iter方法。
        return str(tuple(self))  # 因为该类需要以(x,y)的形式对客户输出，因此用tuple实现，因为tuple的参数必须是可迭代类型，因此要为self的类Vector2d实现__iter__魔法方法

    def __eq__(self, other):
        return tuple(self) == tuple(other)  # 不需要根据Vector2d每个元素一一对比self和other去判断，利用可迭代特性直接比较对象，即利用tuple类型的eq方法。

    def __bytes__(self):
        """
        该方法输出的是 字节串。定义字节串的方法：（1）在字符串前加b以定义字节串，b'XXX'，（2）用bytes([])定义，但bytes类型的元素必须在range(0,256)范围内
        typecode指的是 格式控制字符，例如%s、%d、%f、%e、%c

        bytes方法是用于创建一个字节对象的函数，它接受一个可迭代对象（字符串、整数列表、可变的字节序列）作为参数；
        它返回的字节对象的每个元素都是一个整数，范围在0-255之间。

        ord()函数用于从给定字符值中获取数字值。它接受一个字符并返回一个整数，即用于将字符转换为整数，即用于获取ASCII给定字符的值。
        如果不提前用ord转换为整数再转换为字节对象的话，需要按照 bytes("hello", "ascii")格式将字符串转换为字节对象。

        array(typecode, 可迭代对象)，是为了先得到一个数组，再由bytes转换为字节序列。
        """
        b1 = bytes([ord(self.typecode)])
        b2 = bytes(array(self.typecode, self))
        return b1 + b2

    def __bool__(self):
        # 模为0的不是向量返回False
        return bool(abs(self))


if __name__ == '__main__':
    v1 = Vector2d(3, 4)
    v2 = Vector2d(4.0, 3.0)
    v1_clone = eval(repr(v1))
    print(v1)
    print(abs(v1))
    print(v1 == v1_clone)
    print(v1 == v2)
    print(v1 == [3, 4])
    print(bytes(v2))
    print(bool(Vector2d(0, 0)))
