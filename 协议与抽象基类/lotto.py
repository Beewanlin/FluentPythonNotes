"""
定义LotteryBlower类，是抽象基类Tombola的具体子类。
与BingoCage类的主要区别在于，LotteryBlower类覆盖了继承的inspect方法和loaded方法。
实现方法也有区别：

"""
from 协议与抽象基类.tombola import Tombola

import random


class LotteryBlower(Tombola):

    def __init__(self, iterable):
        self._balls = list(iterable)

    def load(self, iterable):
        self._balls.extend(iterable)

    def pick(self):
        try:
            position = random.randrange(len(self._balls))
        except IndexError:
            raise LookupError('pick from ')
        return self._balls.pop(position)

    def loaded(self):
        return bool(self._balls)

    def inspect(self):
        return tuple(sorted(self._balls))