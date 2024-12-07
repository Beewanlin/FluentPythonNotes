"""
备选构造方法：备选构造方法展示了如何通过类方法提供不同的构造方式,使得对象的创建更富有选择性和适应性。
该例中frombytes实现了从字节序列转换为Vector2d实例的构造方法。使用了classmethod装饰器。

值得一提的是，Python中最常用的两个装饰器：classmethd、staticmethod。
classmethd修饰类方法，常用于定义操作 类(而不是实例)的办法，常用于定义备选构造方法；
staticmethod修饰静态方法，静态方法其实就是碰巧在类的定义体中而不是模块层的普通函数。


本例其他知识点：
array.array.frombytes(b) 是一个属于数组（但不属于列表）的方法。
其作用是：将压缩成机器值的字节序列读出来添加在尾部。

memoryview
常与数组联用的内置类。
其作用是：在不需要复制内容的前提下，在数据结构之间共享内存。实现了用多种不同方式读写同一块内存。
其用法是：使用memoryview.cast('B')方法将同一块内存里的内容(memoryview(array_A))打包成一个全新的memoryview对象。对其memoryview对象的修改最终也会修改原对象。
"""

from array import array
import math


class Vector2d:
    typecode = 'd'  # 类属性-typecode，表示类型码。例如，短整形有符号整数的类型码为'h'，无符号字符的类型码为'B'。

    """
    @classmethod表明这是一个类方法。其一个应用就是给类定义备选构造方法，通过类方法创建对象的实例。
    例如在本例中，该类方法用于从给定的bytes类型数据构造Vector2d实例，并返回时调用构造函数创建类实例。
    最后返回cls(*memv)就是调用构造方法，cls指代类，*memv进行拆包。【拆包】：将可迭代对象（如列表、元组等）按顺序分配到多个变量上。
    
    另一个知识点请联系章节2.9.2 array.array的内置方法frombytes，和内存视图memoryview的用法。
    """
    @classmethod
    def frombytes(cls, octets):
        # 读取octets的字符类型，为其首个字符
        typecode = chr(octets[0])
        # 通过内存视图得到转换了字符类型的字符串对象。memoryview的cast方法会将同一块内存里的东西按照所需要的typoecode打包成一个全新的内存视图给memv。
        memv = memoryview(octets[1:]).cast(typecode)
        # 这里构建了一个新实例。通过类方法实现了另一种构造实例对象的方法。因此该方法也叫做 备选构造方法。
        return cls(*memv)  # 这里是调用类的构造函数，且通过*memv拆包得到分量作为构造函数的参数。

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

    def __eq__(self, other):
        return tuple(self) == tuple(other)  # 不需要根据Vector2d每个元素一一对比self和other去判断，利用可迭代特性直接比较对象

    def __bytes__(self):
        # 该方法输出的是 字节串。定义字节串的方法：（1）在字符串前加b以定义字节串，b'XXX'，（2）用bytes([])定义，但bytes类型的元素必须在range(0,256)范围内
        # typecode指的是 格式控制字符，例如%s、%d、%f、%e、%c
        # ord()函数是Python中的一个库函数，用于从给定字符值中获取数字值。它接受一个字符并返回一个整数，即用于将字符转换为整数，即用于获取ASCII给定字符的值。
        # array(typecode, 可迭代对象)，是为了先得到一个数组，再由bytes转换为字节序列。
        # bytes方法是用于创建一个字节对象的函数，它接受一个可迭代对象（字符串、整数列表、可变的字节序列）作为参数；它返回的字节对象的每个元素都是一个整数，范围在0-255之间
        b1 = bytes([ord(self.typecode)])
        b2 = bytes(array(self.typecode, self))
        return b1 + b2

    def __bool__(self):
        # 模为0的不是向量返回False
        return bool(abs(self))


if __name__ == '__main__':
    v1 = Vector2d(3, 4)
    print(v1)
    # 使用bytes()韩素生成的二进制表示形式重建Vector2d实例，调用类方法。
    v2 = Vector2d.frombytes(bytes(v1))
    print(v2)
