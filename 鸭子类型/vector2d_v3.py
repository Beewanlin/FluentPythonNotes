"""
此例要将Vector2d类优化为 可散列的。
对象要是可散列的，需要满足3个条件：1）实现__hash__()；
2）实现__eq__()方法，这样才能和其他键做比较，相等的对象应该有相等的散列值；
3）对象的散列值不可变，这样才能实现__hash__()方法

由于Vector2d实现了__iter__()方法，其实例是可迭代对象，支持对已初始化的Vector2d类型实例v的分量v.x或v.y更改。不满足上述第三点条件。
因此现在需要将其变为只读对象。
"""

from array import array
import math


class Vector2d:
    typecode = 'd'  # 类属性-typecode，表示类型码。例如，短整形有符号整数的类型码为'h'，无符号字符的类型码为'B'。

    @classmethod
    def frombytes(cls, octets):
        # 读取octets的字符类型，为其首个字符
        typecode = chr(octets[0])
        # 通过内存视图得到转换了字符类型的字符串对象。memoryview的cast方法会将同一块内存里的东西按照所需要的typoecode打包成一个全新的内存视图给memv。
        memv = memoryview(octets[1:]).cast(typecode)
        # 这里构建了一个新实例。通过类方法实现了另一种构造实例对象的方法。因此该方法也叫做 备选构造方法。
        return cls(*memv)

    """
        这里改变了Vector2d实例的分量x和y为私有属性，通过改变__init__()方法中的初始化方法
        并使用@property装饰器赋予类实例读值方法，且读值方法名与属性名相同
        由此改造完成Vector2d.x和Vector2d.y为只读属性。
        """

    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    """
    __hash__()方法应该返回一个整数值，表示散列值。根据Python官方文档的建议，hash最好使用位运算异或混合各分量的散列值计算方法。
    """
    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

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
        b1 = bytes([ord(self.typecode)])
        b2 = bytes(array(self.typecode, self))
        return b1 + b2

    def __bool__(self):
        # 模为0的不是向量返回False
        return bool(abs(self))


if __name__ == '__main__':
    v1 = Vector2d(3, 4)
    v2 = Vector2d(3.1, 4.2)
    print(hash(v1))
    print(hash(v2))
    # 当前Vector2d是可散列的，因此可以放在集合set里
    print(set([v1, v2]))
