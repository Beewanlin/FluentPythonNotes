"""
TomboList是Tombola的虚拟子类 和 list的真实子类。
注册虚拟子类的方式是在抽象基类上调用register方法。可用装饰器的方式注册，也可以作为普通的函数调用。
这种是一种，无需在继承关系中确立静态的强链接，就可以子类化抽象基类或使用抽象基类注册的方式。
"""
import random

from 协议与抽象基类.tombola import Tombola


@Tombola.register
class TomboList(list):

    def pick(self):
        if self:  # 这里利用了继承自list的bool方法，如果不为空返回True
            position = random.randrange(len(self))
            return self.pop(position)
        else:
            raise LookupError('pop from empty TomboList')

    load = list.extend  # 定义load等于list.extend函数

    def loaded(self):
        return bool(self)  # 使用内置的bool方法给出判断结果（内置的bool方法通过__len__判断是否为True）

    def inspect(self):
        return tuple(sorted(self))


# 另一种注册抽象基类的子类的方法：直接调用抽象基类的register方法，并将虚拟子类作为参数。如下：
# Tombola.register(TomboList)


if __name__ == '__main__':
    print(issubclass(TomboList, Tombola))
    t = TomboList(range(10))
    print(isinstance(t, Tombola))
    print(TomboList.__mro__)  # 类的属性__mro__记录了类的继承关系
