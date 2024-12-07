"""
此例基于《序列-vecotr_v5》代码，新增对以下运算符的重载。
一元运算符：
- ：一元取负运算符，由方法__pos__()支持
+ ：一元取正运算符，由方法__neg__()支持
～ ：一元取反运算符
中缀运算符：
+ ：加法运算符，由方法__add__()支持
* ：乘法运算符（本例中只实现标量乘法运算符），由方法__mul__()支持
= ：比较运算符，由方法__eq__()支持

需注意：中缀运算符方法的返回值都是新建的对象，其基本原则就是不改变操作对象，只读取操作对象的值，运算后产出一个新的值返回。除了增量运算符（就地运算符），会处理self。
"""
import itertools
from array import array
import reprlib
import math
import functools
import operator
import numbers


class Vector:
    typecode = 'd'

    def __init__(self, components):
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return 'Vector({})'.format(components)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return bytes([ord(self.typecode)]) + bytes(self._components)

    def __eq__(self, other):
        """
        改进Vector方法的__eq__方法
        上一版本的方法会忽略类型检查，对于长度相同且元素相同的可迭代对象会判断为相等。
        这版需要进行改进：如果第二个操作数是Vector实例或其子类，则用__eq__方法，否则返回NotImplemented，让Python解释器去做后续处理。
        Python后续会如何处理呢？当左操作数的__eq__方法得到返回NotImplemented后，会去调用右操作数的__eq__方法，如果也得到返回NotImplemented，则会比较两者id()
        """
        if isinstance(other, Vector):
            return len(self) == len(other) and all(a == b for a, b in zip(self, other))
        else:
            return NotImplemented

    def __ne__(self, other):
        """
        由于已经实现了__eq__方法，可以利用Python解释器自己的处理：__ne__有后备处理机制 返回 __eq__相反的结果。
        可以不用特实现__ne__方法。其实现原理类似下面这段代码逻辑，是基于__eq__实现的。
        """
        eq_result = self == other
        if eq_result is NotImplemented:
            return NotImplemented
        else:
            return not eq_result

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self._components))

    def __bool__(self):
        return bool(abs(self))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)

    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(index, int):
            return self._components[index]
        else:
            msg = '{cls.__name__} indices must be integers'
            raise TypeError(msg.format(cls=cls))

    shortcut_names = 'xyzt'

    def __getattr__(self, name):
        cls = type(self)
        if len(name) == 1:
            pos = cls.shortcut_names.find(name)
            if 0 <= pos < len(self._components):
                return self._components[pos]
        msg = '{.__name__!r} object has no attribute{!r}'
        raise AttributeError(msg.format(cls, name))

    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:
            if name in cls.shortcut_names:
                error = 'readonly attribute {attr_name!r}'  # 报错该属性为只读
            elif name.islower():
                error = "cannot set attributes 'a' to 'z' in {cls_name!r}"
            else:
                error = ''
            if error:
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)
        super().__setattr__(name, value)

    def __hash__(self):
        hashes = (hash(x) for x in self._components)
        return functools.reduce(operator.xor, hashes, 0)

    def angle(self, n):
        r = math.sqrt(sum(x * x for x in self._components[n:]))
        a = math.atan2(r, self[n - 1])
        if n == len(self) - 1 and self[-1] < 0:
            return math.pi * 2 - a
        else:
            return a

    def angles(self):
        return (self.__angle__(n) for n in range(1, len(self)))

    def __format__(self, format_spec=''):
        if format_spec.endswith('h'):
            format_spec = format_spec[:-1]
            coords = itertools.chain(abs(self), self.angles())  # itertools.chain()方法拼接列表/字典/元组/集合等可迭代对象（可混拼）成为一个新的可迭代对象
            outer_fmt = '<{}>'
        else:
            coords = self
            outer_fmt = '({})'
        components = (format(c, format_spec) for c in coords)
        return outer_fmt.format(', '.join(components))

    def __pos__(self):
        """一元取正运算符，返回其本身"""
        return Vector(self)

    def __neg__(self):
        """一元取反运算符，其每个分量都取反"""
        return Vector(-x for x in self)

    def __add__(self, other):
        """
        希望支持不同长度向量的相加，对长度不足的做补零的处理。这里需要用到itertools.zip_longest方法(*iterables, fillvalue)。
        该方法会创建一个迭代器，聚合来自每个可迭代对象的元素。如果可迭代的长度不均匀，则补充fillvalue替代缺失值。迭代一直持续到最长的可迭代对象用完为止。

        由于可能遇到不支持操作数类型的情况，需要进行处理。这里对于操作数的要求是可迭代对象，可迭代对象很多种难以列出和判断，因此适合用鸭子类型的思想。
        鸭子类型实现方法：对于TypeError来说，最好的处理办法是将它捕获并返回NotImplemented，这样解释器会尝试调用反向运算符方法。而不是判断操作数类型。
        """
        try:
            pairs = itertools.zip_longest(self, other, fillvalue=0.0)  # 返回一个生成器，生成(a, b)形式的元组。
            return Vector(a+b for a, b in pairs)  # 用生成器表达式来计算pairs中各元素的值。
        except TypeError:
            return NotImplemented

    def __radd__(self, other):
        """
        此方法是__add__()的后备方法，为了解决左操作数是其他类型但右操作数是Vector类实例时的加法运算。
        简单实现方法，即直接委托给__add__()方法（对任何可交换的运算符都可以这么处理__radd__()方法）。
        """
        return self + other

    def __mul__(self, scalar):
        """
        本也可以像实现__add__()方法一样，对于不支持的操作数捕获异常。但这里所支持操作数的类型很明确，标量可能是整数、浮点数、bool、fractions.Fraction。
        因此适合用白鹅类型实现，即直接判断操作数的类型。
        numbers.Real是int、float、bool、fractions.Fraction的抽象基类
        """
        if isinstance(scalar, numbers.Real):
            return Vector(n*scalar for n in self)  # 这里判断 scalar 是否是 numbers.Real的子类
        else:
            return NotImplemented

    def __rmul__(self, scalar):
        return self * scalar


if __name__ == '__main__':
    v1 = Vector(range(7))
    v2 = Vector([0, 1, 2, 3, 4, 5, 6])
    # 加法
    print(v1 + v2)
    v3 = Vector([6, 7, 8, 9])  # 支持不同长度的Vector实例相加
    print(v1 + v3)
    v4 = (2, 3, 4, 5)  # 注意这是元组
    print(v1 + v4)  # 支持，v4作为__add__函数中的other参数，itertools.zip_longest支持各种类型的可迭代对象
    """
    若没有实现Vector的__radd__()方法，那么左操作数是非Vector类实例时，会返回TypeError错误。
    v4 + v1 不支持，v4并不是Vector类型，不会调用Vector重载的__add__方法，调用的是tuple类型的原生的_add__方法，该方法不支持混合类型的加法。
    若实现了Vector的__radd__()方法，那么左操作数是非Vector类实例时，调用tuple的__add__方法会返回NotImplemented，此时会再调用右操作数的__radd__()方法。
    """
    print(v4 + v1)
    # 乘法
    print(v1 * 3)
    print(2 * v1)
    print(v1 * v2)

