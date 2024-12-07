"""
该例使用生成器实现Sentence类，这是一种更常用的方式。


1）对比之前版本的定义一个迭代器类，iter返回一个迭代器对象，
此版本的iter返回一个生成器对象（生成器也是迭代器），该例中的iter方法实际上是生成器函数，返回一个生成器对象。
2）对比之前版本的next(迭代器)返回迭代器中下一个元素，
此版本把生成器传给next()，生成器函数会向前执行函数定义体中的下一个yield语句，返回产出的值，并在函数定义体的当前位置暂停;
直到下一次next调用，再继续向前执行到下一个yiedl语句。
生成器函数的定义体返回时，外层生成器对象会抛出StopIteration异常（这一点与迭代器相同）。

(for循环迭代时会隐式调用next())

"""

import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:

    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        """
        该方法区别与上一版sentence_iter在于，不需要再单独定义一个迭代器类，而是返回一个生成器对象作为迭代器
        该函数__iter__()其实是一个生成器函数（定义体中带有关键词yield的就是生成器函数），返回一个生成器对象。
        """
        for word in self.words:
            yield word
        return  # 该语句可以省略，生成器生成完全部值后会自动退出

