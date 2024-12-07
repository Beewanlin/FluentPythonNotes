"""
该例中，实现动态存取属性。
动态获取属性，可以实现__getattr__方法。
通常来说，实现了__getattr__方法，也要定义__setattr__方法，以防止对象的行为不一致。


（更重要的知识点是 属性查找机制，在v6中详细说明。）
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


if __name__ == '__main__':
    v1 = Vector(range(7))
    # 已实现__getattr__方法，可通过单个字母访问Vector的前几个分量
    print(v1)
    print(v1.x)
    # 下面这里应该要报错，并控制不能为名称是xyzt或其他单个小写字母的属性赋值，否则会造成误以为赋值成功的误会，v.x的值前后错乱。
    # 应实现__setattr__方法：如果为名称是xyzt或其他单个小写字母的属性赋值，则抛出AttributeError异常。
    v1.x = 10
    print(v1.x)
    print(v1)
