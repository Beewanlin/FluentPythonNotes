"""
该例说明了如果继承自内置类型dict，会出现内置类型的方法忽略覆盖方法的问题。
"""


class DoppelDict(dict):
    # 覆盖 __setitem__方法
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)


if __name__ == '__main__':
    dd = DoppelDict(one=1)   # 类DoppleDict继承自dict的__init__方法本要调用__setitem__方法，但是实际上直接忽略了这个覆盖方法。
    print(dd)
    dd['two'] = 2
    print(dd)
    dd.update(three=3)   # 类DoppleDict继承自dict的方法update本要调用__setitem__方法，但是实际上直接忽略了这个覆盖方法。
    print(dd)
