"""
该例中，列举自定义序列类型的切片实现。
由此，我们应该模仿切片原理，即slice内置类型，其有3个属性：start、stop、step，还有一个方法为indices(len)用于优雅处理缺失索引和负数索引以及长度超过目标序列的切片
"""

from array import array
import reprlib
import math


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

    def __eq__(self, other):
        return tuple(self) == tuple(other)

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


if __name__ == '__main__':
    v1 = Vector(range(7))
    v2 = v1[1:4]
    v3 = v1[0]
    v4 = v1[1, 2]  # 会报错，因为其入参只支持slice类型和int类型
    print(v1)  # 输出的是(0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0)，表示v1是Vector实例
    print(v2)  # 输出的是(1.0, 2.0, 3.0)，表示v2也是一个Vector实例
    print(v3)
