"""
这个版本使用迭代器模式实现Sentence类。
该例中，会实现典型的迭代器，会揭示可迭代对象和迭代器明细的区别：
Sentence是一个可迭代类，其实例是可迭代对象，其必须要实现的方法只有__iter__()方法，每次返回都是实例化一个新的迭代器；
SentenceIterator是一个迭代器，其必须要实现__next__()方法和__iter__()方法，并且，next方法返回迭代器中下一个元素，iter方法返回迭代器本身；
因此，迭代器可以迭代，但是可迭代对象不是迭代器。
而且，可迭代对象一定不能是自身的迭代器。因此，可迭代对象一定要实现__iter__方法，但不能实现__next__方法。
"""

import re
import reprlib

RE_WORD = re.compile('\w+')


# 和上一版一样为了定义一个可迭代类。根据可迭代协议，需要实现__iter__方法
class Sentence:

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.split(text)

    def __repr__(self):
        # 原来是 return 'Sentence(%s)' % self.text
        return 'Sentence(%s)' % reprlib.repr(self.text)  # reprlib.repr 与 内置方法 repr() 类似，只不过增加了不同类型的长度限制，避免产生超长的表示

    def __iter__(self):
        return SentenceIterator(self.words)  # iter方法返回一个迭代器


# 定义一个迭代器类，根据定义，迭代器需要实现接口__next__()、__iter__()
class SentenceIterator:

    def __init__(self, words):
        self.words = words
        self.index = 0

    def __next__(self):
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return word

    def __iter__(self):
        return self
