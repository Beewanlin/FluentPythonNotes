"""
定义一个抽象基类：
声明一个抽象基类，最好的办法是继承自abc.ABC
定义抽象方法，需要用到装饰器@abc.abstractmethod（注意，堆叠装饰器也有顺序要求，@abc.abstractmethod应放在最里层）
"""

import abc


class Tombola(abc.ABC):

    @abc.abstractmethod
    def load(self, iterable):
        """从可迭代对象中添加元素"""

    @abc.abstractmethod
    def pick(self):
        """
        随机删除元素，然后将其返回；
        如果实例为空，这个方法应该抛出异常'LookupError'
        """

    def loaded(self):
        """如果至少有一个元素，返回True，否则返回False"""
        return bool(self.inspect())

    def inspect(self):
        """返回一个有序元组，由当前元素构成"""
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)
        return tuple(sorted(items))