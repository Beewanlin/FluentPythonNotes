"""
该例中，将实现Vector类的格式化显示，使用超球面坐标，格式说明符号为'h'（意为hyperspherical coordina，避免与内置的格式说明符重用）
"""
import itertools
from array import array
import reprlib
import math
import functools
import operator


class Vector:
    typecode = 'd'

    """
    构造函数，接收可迭代对象作为参数。
    参数是Vector的分量，存入array数组中。
    """

    def __init__(self, components):
        self._components = array(self.typecode, components)

    """
    使用self._components构建一个迭代器。
    iter()和__iter__将在后续说明？？？？
    """

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

    """"
    对于维数很多的向量，比较两个向量时用tuple的__eq__方法会浪费内存和时间。
    为了提高比对的效率，改进__eq__方法。
    利用zip函数生成元组生成器，来节省内存和时间。
    """

    def __eq__(self, other):
        # if len(self) != len(other):
        #     return False
        # for a, b in zip(self, other):
        #     if a != b:
        #         return False
        # return True
        # 以上写法可以由all函数大大简化，如下：
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self._components))  # 最后self._components可简化为self？

    def __bool__(self):
        return bool(abs(self))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)  # 因为Vector类的构造函数入参为可迭代对象，因此这里传参不需要使用*拆包了

    """
    实现__len__和__getitem__方法，实现序列协议。
    """

    def __len__(self):
        return len(self._components)

    # 改进__getitem__方法，使得切片后得到的对象类型还是原类型Vector
    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(index, int):
            return self._components[index]
        else:
            msg = '{cls.__name__} indices must be integers'
            raise TypeError(msg.format(cls=cls))

    """
    想要实现 通过单个字母访问Vector类实例的前几个分量，可以用__getattr__方法
    """
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
        # 名称是xyzt或其他单个小写字母的属性，需要各自抛出异常
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
        # 其他情况，调用超类的方法设置属性
        super().__setattr__(name, value)

    """
    这里的散列方法是 映射规约，即对每个分量的散列值计算异或。
    散列，要用到Python内置的hash函数，这里用生成器表达式产出hash结果，节省内存。
    归约，要使用到reduce，其参数有三个，分别是：操作函数、可迭代对象、初始值（对于+、|、^来说，初始值应为0；对于*、&来说，初始值应为1）
    
    """

    def __hash__(self):
        hashes = (hash(x) for x in self._components)
        return functools.reduce(operator.xor, hashes, 0)

    def angle(self, n):
        # 根据数学公式计算超维向量的某个角的角度
        r = math.sqrt(sum(x * x for x in self._components[n:]))
        a = math.atan2(r, self[n - 1])
        if n == len(self) - 1 and self[-1] < 0:
            return math.pi * 2 - a
        else:
            return a

    def angles(self):
        # 获取超维向量每个角的角度 存在可迭代对象中
        return (self.__angle__(n) for n in range(1, len(self)))

    """
    format支持向量格式输出-格式说明符为空，也支持超球体坐标输出-格式说明符为h（其表现形式为：<r, thita1, thita2, thita3>）。
    angle函数和angles辅助计算超球体坐标需要的角度值。
    
    其他知识点：
    itertools.chain
    """

    def __format__(self, format_spec=''):
        if format_spec.endswith('h'):
            format_spec = format_spec[:-1]
            coords = itertools.chain(abs(self), self.angles())  # 使用itertools.chain生成 生成器表达式，无缝迭代向量的模和各个角
            outer_fmt = '<{}>'
        else:
            coords = self
            outer_fmt = '({})'
        components = (format(c, format_spec) for c in coords)
        return outer_fmt.format(', '.join(components))


if __name__ == '__main__':
    v1 = Vector(range(7))
    v2 = Vector([0, 1, 2, 3, 4, 5, 6])
    print(v1 == v2)
