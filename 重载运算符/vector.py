"""
这里实现基本 vector 类，使其有加、乘、bool、计算绝对值的方法
"""
import math


class Vector:

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        print('Vector(%r, %r)' % (self.x, self.y))

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        if self.__abs__():
            return True
        else:
            return False

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Vector(scalar * self.x, scalar * self.y)