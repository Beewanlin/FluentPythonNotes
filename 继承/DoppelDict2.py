"""
这里通过继承Python实现的类 collections.UserDict，就能按照预判那样，自定义类调用的是覆盖后的函数。
"""

import collections


class DoppelDict2(collections.UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)


if __name__ == '__main__':
    dd = DoppelDict2(one=1)  # 类DoppleDict2继承自dict的__init__方法本会调用覆盖后的__setitem__方法
    print(dd)
    dd['two'] = 2
    print(dd)
    dd.update(three=3)  # 类DoppleDict2继承自collections.UserDict的方法update会要调用覆盖后的__setitem__方法
    print(dd)
