"""
此例基于《协议与抽象基类-bingo》代码，新增对以下运算符的重载。
增量运算符：
+= ：如果实现了就地运算符方法__iadd__，则会调用该方法，否则就是语法糖，最终调用的还是__add__。注意，不可变类型不能实现就地运算符方法。
"""
from 协议与抽象基类.tombola import Tombola
from 协议与抽象基类.bingo import BingoCage

class AddableBingoCage(BingoCage):

    def __add__(self, other):
        # 进行类型检查
        if isinstance(other, Tombola):
            return AddableBingoCage(self.inspect() + other.inspect())
        else:
            return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, Tombola):
            other_iterable = other.inspect()
        else:
            try:
                other_iterable = iter(other)
            except TypeError:
                self_cls = type(self).__name__
                msg = "right operand in += must be {!r} or an iterable."
                raise TypeError(msg.format(self_cls))
        self.load(other_iterable)
