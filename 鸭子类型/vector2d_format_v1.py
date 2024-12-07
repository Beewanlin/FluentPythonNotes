"""
格式化显示-2种方法：
1.format(ori, format_spec)
2."...{ori_var: format_spec}".format(ori_var=ori)

format_spec是格式说明符，其表示法叫做格式规范微语言。
对于一些内置类型来说，格式规范微语言有专门的表示代码，例如：b表示二进制int类型，x表示十六进制int类型，f表示小数形式的float类型，而%表示百分数形式。
而格式规范微语言是可扩展的，可以在类中自行决定如何解释format_spec参数。
以上格式化显示的2种方法，其实都是委托给方法 __format__()。

在自定义的类中，需要实现自己的格式规范微语言以传入格式说明符，通过定义__format__() 方法来实现。
如果在类中没有定义 __format__() 方法，则会返回str(object)，那么调用format(object)是不允许带format_spec参数，否则会抛出TypeError异常。

如果对于 Vector2d 类来说，想要实现format(v)、format(v, form_spec)，应定义__format__() 方法如下：
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
        return math.hypot(self.x, self.y)  # math包中有专门的函数 用来计算直角三角形的斜边长

    def __repr__(self):
        class_name = type(self).__name__
        return "{}({}, {})".format(class_name, *self)  # 这里 *self 会将x和y分量提供给format函数。

    def __str__(self):
        # return str((self.x, self.y))
        return str(tuple(self))  # 直接用tuple改进实现，因为tuple的参数必须是可迭代类型，因此要为self的类Vector2d实现__iter__魔法方法

    """
    自定义格式化函数，重写内置的__format__()方法。
    在此例中，要求format函数将fmt_spec应用到向量的各个分量上，并仍按照格式(x,y)输出。
    fmt_spec默认为空，或填入格式说明符参数例如'.2f'、'.3e'，则分量会按照格式2位小数浮点数、3位小数科学计数法显示。
    """
    def __format__(self, format_spec=''):
        components = (format(c, format_spec) for c in self)  # 对每个分量进行格式化
        return "({}, {})".format(*components)  # 按照格式输出

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


if __name__ == '__main__':
    v1 = Vector2d(3, 4)
    print(format(v1))
    print(format(v1, '.2f'))
    print(format(v1, '.3e'))
