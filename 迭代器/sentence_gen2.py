"""
该版本改进了惰性实现，优化初始化函数一次性生成单词列表的"及早求值"，改进为生成生成器的"惰性求值"。

re.findall()的惰性求值版本是re.finditer()，它返回一个生成器。
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
        在生成器函数中调用re.finditer()生成器函数。
        不再需要在初始化时生成words列表了。
        RE_WORD.finditer()返回
        """
        for match in RE_WORD.finditer(self.text):
            yield match.group()  # match.group()方法从MatchObject实例中提取匹配正则表达式的具体文本
        return


if __name__ == '__main__':
    s = Sentence('I love sunny days')
    print(s)
    for word in s:
        print(word)