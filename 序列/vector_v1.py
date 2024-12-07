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
    
    注意第二个方法，不够完美，应该模仿Python的做法——内置序列切片得到的各自新实例也是内置序列。 
    """

    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        return self._components[index]  # 注意此处返回的是数组，而不是序列，因为self._components是数组类型。


if __name__ == '__main__':
    v1 = Vector(range(7))
    v2 = v1[1:4]
    v3 = v1[0]
    print(v1)  # 输出的是(0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0)，表示v1是Vector实例
    print(v2)  # 输出的是 array('d', [1.0, 2.0, 3.0])，表示v2是一个数组
    print(v3)
