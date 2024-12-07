"""
定义BingoCage类，是抽象基类Tombola的具体子类。
直接继承了Tombola类的loaded方法和inspect方法。
实现方法：
初始化调用了load方法对空列表逐个添加元素并打乱顺序；
load方法添加一个元素（并没有要求顺序，因此可以在此打乱顺序）；
pick取函数时，取列表最后一个，实际效果上是实现了随机删除一个元素；
"""
from 协议与抽象基类.tombola import Tombola

import random


class BingoCage(Tombola):

    def __init__(self, items):
        self._randomizer = random.SystemRandom()  # 随机发生器
        self._items = []
        self.load(items)  # 借用load方法实现初次加载

    def load(self, items):
        self._items.extend(items)
        self._randomizer.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:  # IndexError是LookupError的子类
            raise LookupError('pick from empty BingoCage')  # 抛出明确异常

    def __call__(self):
        """添加在Tombola接口额外的方法。为了给BingoCage.pick()添加快捷的调用方式：BingoCage实例bingo()即可调用"""
        self.pick()