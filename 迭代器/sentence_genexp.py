"""
该版本在使用re.finditer()改进了惰性实现的基础上，进一步优化"惰性求值"。

生成器表达式是替代生成器函数的语法糖，类似列表推导替代for循环；列表推导是制造列表的工厂，生成器表达是制造生成器的工厂。
生成器其实是列表推导式的惰性版本，列表推导会立即生成一个列表占用更多内存。
"""

import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        """
        上个版本是在生成器函数内的for循环中每次迭代时，获取一个匹配结果MatchObject实例；
        此版本进一步改进，更惰性一点，使用生成器表达式替代生成器函数。
        """
        return (match.group() for match in RE_WORD.finditer(self.text))


if __name__ == '__main__':
    s = Sentence('I love sunny days')
    print(s)
    for word in s:
        print(word)