"""
此例中，我们想自定义一种格式函数 使得实例以【极坐标】形式表示。
"""

from array import array
import math


class Vector2d:
    typecode = 'd'  # 类属性-typecode，表示类型码。例如，短整形有符号整数的类型码为'h'，无符号字符的类型码为'B'。

    @classmethod
    def frombytes(cls, octets):  # 定义备用构造方法。用于从给定的bytes类型数据构造Vector2d实例。
        typecode = chr(octets[0])
        memv = memoryview(octets[:]).cast(typecode)  # 内存视图。其cast方法会将同一块内存里的东西按照所需要的typoecode打包成一个全新的内存视图给memv。
        return cls(*memv)

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __iter__(self):
        # 为了实现拆包，从Vector2d实例中产出分量self.x 和 self.y，需要将Vector2d实例实现为可迭代的。
        return (i for i in (self.x, self.y))

    def __abs__(self):
        return math.hypot(self.x, self.y)  # math包中有专门的函数 用来计算直角三角形的斜边长。在这里相当于计算向量的模

    def __repr__(self):
        class_name = type(self).__name__
        return "{}({}, {})".format(class_name, *self)  # 这里 *self 会将x和y分量提供给format函数。

    def __str__(self):
        # return str((self.x, self.y))
        return str(tuple(self))  # 直接用tuple改进实现，因为tuple的参数必须是可迭代类型，因此要为self的类Vector2d实现__iter__魔法方法

    """
    自定义格式化函数，重写内置的__format__()方法。
    在此例中，要求format函数除了支持按照原先的直角坐标系输出，也支持以'p'结尾的格式说明符参数，按照极坐标格式(abs, angle)输出。
    fmt_spec若为以p结尾的格式说明符，就是极坐标系格式输出。
    """
    def __format__(self, format_spec=''):
        if format_spec.endswith('p'):
            format_spec = format_spec[:-1]
            coords = (abs(self), self.angle())
            outer_fmt = '<{},{}>'
        else:
            coords = self
            outer_fmt = '({},{})'
        components = (format(c, format_spec) for c in coords)  # 对每个分量进行格式化
        return outer_fmt.format(*components)  # 按照格式输出

    def __eq__(self, other):
        return tuple(self) == tuple(other)  # 不需要根据Vector2d每个元素一一对比self和other去判断，利用可迭代特性直接比较对象

    def __bytes__(self):
        # 该方法输出的是 字节串。定义字节串的方法：（1）在字符串前加b以定义字节串，b'XXX'，（2）用bytes([])定义，但bytes类型的元素必须在range(0,256)范围内
        # typecode指的是 格式控制字符，例如%s、%d、%f、%e、%c
        # ord()函数是Python中的一个库函数，用于从给定字符值中获取数字值。它接受一个字符并返回一个整数，即用于将字符转换为整数，即用于获取ASCII给定字符的值。
        b1 = bytes([ord(self.typecode)])
        b2 = bytes(array(self.typecode, self))
        return b1 + b2

    def __bool__(self):
        # 模为0的不是向量返回False
        return bool(abs(self))

    """
    此例为了自定义 极坐标 的格式化显示，除了已有的abs取模函数，还需要计算角度。
    """
    def angle(self):
        return math.atan2(self.y, self.x)  # atan反三角函数，计算角度


if __name__ == '__main__':
    v1 = Vector2d(3, 4)
    print(format(v1))
    print(format(v1, 'p'))
    print(format(v1, '.5fp'))
    print(format(v1, '.3ep'))
