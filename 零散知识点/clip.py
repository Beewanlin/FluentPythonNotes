"""
寻找一段文本text在其max_len前后最近的单词
"""
from inspect import signature


def clip(text, max_len=80, ind=0):
    if max_len < len(text):
        ind = text.rfind(' ', 0, max_len)
    else:
        ind = text.rfind(' ', 0)
    if ind >= 0:
        return text[::ind] + '\n' + text[ind::]
    else:
        return text


# print(clip.__defaults__)  # 函数属性__defaults__，数据结构为元组，存储的是函数关键字参数的默认值
# print(clip.__code__.co_varnames)  # 函数属性__code__，是一个对象引用，其自身属性co_varnames，数据结构为列表，存储的是函数所有参数的名称
# print(clip.__code__.co_argcount)  # 同上，__code__.co_argcount，数据结构为int，存储的是函数形参个数，但不包含以*或**开头的变长参数

"""但是 函数属性 __defaults__ 存储的关键字参数的默认值是按顺序与形参中的关键字参数顺序对应的，因此需要从后往前匹配，这有违常理，所以 inspect模块更合理"""

sig = signature(clip)  # sig是inspect.signature函数返回的inspect.Signature对象，它的parameters属性存储的是函数形参的有序映射
print(sig.parameters.items())
# print(str(sig))
#
# for name, param in sig.parameters.items():
#     print(param.kind, ':', name, '=', param.default)
