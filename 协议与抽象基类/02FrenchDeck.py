"""
该例定义的类FrenchDeck-纸牌，实现了序列协议。但序列协议也分为 可变的序列协议 和 不可变的序列协议。
如果仅实现__getitem__而没有实现__setitem__方法，那么仅为 不可变的序列协议；需要实现__setitem__方法，才是可变的序列协议。
"""
import collections
from random import shuffle  # 提前导入了random.shuffle，序列可以直接使用该方法，不需要自己再去实现shuffle方法。

Card = collections.namedtuple('Card', ['rank', 'suit'])  # 定义一个具名元组，两个参数，分别是字符串（元组名）、列表（字符串类型的元组元素名，逗号隔开）


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]  # 二维遍历

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, pos):
        return self._cards[pos]

    """
    只实现__getitem__而不实现__setitem__，那么只实现了【不可变的序列协议】；
    若要支持为元素赋值，需要实现__setitem__方法。
    """
    def __setitem__(self, key, value):
        self._cards[key] = value


if __name__ == '__main__':
    f = FrenchDeck()
    print(len(f))
    print(f[1])
    shuffle(f)  # random.shuffle函数不关心参数的类型，只要f对象实现了部分可变序列协议可以。
