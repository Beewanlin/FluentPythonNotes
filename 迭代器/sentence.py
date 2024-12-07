"""
实现一个 单词序列
创建一个sentence类，该类实例是一个可迭代对象，该类的主要作用是将句子划分为词。
"""
import re
import reprlib

# 生成正则表达式 pattern对象。该正则表达式的匹配规则为：匹配数字或字母或符号1次或多次
RE_WORD = re.compile('\w+')


class Sentence:

    def __init__(self, text):
        # 构造方法，传入一个字符串
        self.text = text
        # re.findall返回包含所有匹配项的列表
        self.words = RE_WORD.findall(text)

    def __getitem__(self, index):
        return self.words[index]

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)


if __name__ == '__main__':
    text = 'The winter is coming...'
    s = Sentence(text)
    print(s)
    print(s.words)
    print(len(s))
