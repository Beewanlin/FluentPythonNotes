"""
定义一个装饰器，用来预激活协程
"""


from functools import wraps


def coroutine(func):
    @wraps(func)  # 作用是保护被装饰函数的原有属性__name__、__doc__不被装饰器改变
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return primer


